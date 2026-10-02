phyHUB CLI Manual: Devices & Software
=====================================

This guide walks you through the phyHUB command-line client, ``m2cp``, from
claiming a freshly provisioned device to installing software on it, watching
updates roll out, and, for developers, publishing your own software, models, and
seeds.

It is the developer-focused counterpart to the phyHUB **UI Manual**. Everything
here happens from your terminal. Asset management (asset types, models,
instances, commissioning, attribute sets) is **UI-only** and is not covered by
the CLI. See the UI Manual for that.

--------------

How Everything Connects: The Big Picture
----------------------------------------

The CLI talks to the same phyHUB backend (“the store”) that the web UI
does. Two command trees do most of the work::

     m2cp device …   →  operate on a single edge device
                        (claim, rename, inspect, watch updates, reboot)

     m2cp store  …   →  operate on the store / catalog
                        (deployment groups, apps, snaps, software, models)

     m2cp user   …   →  authentication (login, status)

The onboarding flow, in the order this manual follows::

   Physical device  →  Provisioned on the device (terminal, claiming token)
          │
          ▼
   m2cp device claim <token>          Register it in the store
          │
          ├──▶  m2cp device modify … --name        Give it a friendly name
          │
          ├──▶  m2cp store dgroup create …          Create a Deployment Group
          │           │
          │           └──▶  m2cp store dgroup software add …   List its apps
          │
          └──▶  m2cp device dgroup set <dev> <grp>  Join the group
                      │
                      └──▶  apps install automatically → watch with
                            m2cp device update follow

Key concepts, in plain language:

+-----------------------------------+-------------------------------------------+
| Concept                           | What it is                                |
+===================================+===========================================+
| **Device**                        | A physical edge device (e.g. a phyBOARD / |
|                                   | Raspberry Pi–class gateway) registered    |
|                                   | with the store. Identified by an          |
|                                   | **OS-Serial** (a UUID) and, optionally, a |
|                                   | friendly **name**                         |
+-----------------------------------+-------------------------------------------+
| **App / Snap**                    | A snap package that runs on a device.     |
|                                   | Uploaded to the store, rated, then        |
|                                   | deployed                                  |
+-----------------------------------+-------------------------------------------+
| **Software**                      | The store's umbrella term (store ≥ 5.3.0) |
|                                   | covering both **apps** (snaps) and the    |
|                                   | **OS image** (e.g. ``phytec-liot-image``) |
|                                   | that ships via RAUC                       |
+-----------------------------------+-------------------------------------------+
| **Deployment Group (dgroup)**     | A named group of devices of one model     |
|                                   | that share the same target set of         |
|                                   | software. Adding a device installs the    |
|                                   | group’s software on it automatically      |
+-----------------------------------+-------------------------------------------+
| **Model**                         | The device model definition (type, name,  |
|                                   | revision, architecture, and the snaps it  |
|                                   | ships with). Devices of a given model can |
|                                   | join dgroups built for that model         |
+-----------------------------------+-------------------------------------------+
| **Update Action**                 | One unit of change the backend calculates |
|                                   | for a device: install, update, or delete  |
|                                   | a piece of software. It moves through     |
|                                   | phases you can inspect and follow live    |
+-----------------------------------+-------------------------------------------+
| **Rating**                        | A software version’s release status:      |
|                                   | **Experimental**, **Edge**, or **Stable** |
|                                   | (all deployable) or **Denied** (not       |
|                                   | deployable). Freshly uploaded versions    |
|                                   | are **Unrated**                           |
+-----------------------------------+-------------------------------------------+
| **Seed**                          | A snapd seed: the set of snaps + model    |
|                                   | baked into a **custom OS image** at build |
|                                   | time. Generated with                      |
|                                   | ``m2cp store system snapd-seed generate`` |
+-----------------------------------+-------------------------------------------+

--------------

Before You Begin
----------------

Install and authenticate
~~~~~~~~~~~~~~~~~~~~~~~~

``m2cp`` is delivered as a Debian package. Install it, then log in against your
store's GraphQL endpoint:

.. code:: console

   # Browser-based login (opens your browser to authenticate)
   host:~$ m2cp user login --store https://api.phyhub.phytec.de/graphql --method browser

   # Confirm who you are and which store you are pointed at
   host:~$ m2cp user status

``m2cp`` remembers your store and session, so subsequent commands need no
``--store`` flag.

Provision the device first
~~~~~~~~~~~~~~~~~~~~~~~~~~

This step happens on the device, before you touch ``m2cp``.

A freshly imaged device runs the provisioning flow and prints a **claiming
token** on its console. For example::

   +--------------------------------------+
   |    Enter this token in the L-IoT     |
   |     Appstore to bind this device     |
   |           to your account:           |
   |                                      |
   |            PBTK-Q9SH-4N2B            |
   |                                      |
   +--------------------------------------+
   [09:25:37] Waiting for you to enter the token in the L-IoT Appstore...

Once you claim that token (next section), the device reports back::

   [09:26:50] Device registered (OS-Serial: 73fe2304-6be9-5f4a-8086-bffcbe38f930)

Full provisioning instructions are in the **Device Provisioning Manual**.
Complete that first, then continue here.

CLI conventions
~~~~~~~~~~~~~~~

A few things that apply to every command:

-  **Aliases** save typing: ``device`` → ``d``, ``store`` → ``s``, ``dgroup`` →
   ``d``, ``software`` → ``sw``. So ``m2cp d info demo-device`` == ``m2cp device
   info demo-device``.
-  **Devices can be addressed by OS-Serial or name** wherever a device argument
   is accepted (once you’ve named them).
-  ``--json`` is a global flag on every command; add it for machine-readable
   output you can pipe into ``jq``.
-  Most write commands return a **``Task-Id``** and a confirmation line; that ID
   is the backend job that carried out your request.
-  ``-h``/``--help`` works at every level:

   .. code-block:: console

      host:~$ m2cp store dgroup software add --help``.

--------------

Part 1: Onboarding a Device
---------------------------

Claim the device
~~~~~~~~~~~~~~~~

Feed the claiming token from the device console to ``claim``:

.. code:: console

   host:~$ m2cp device claim PBTK-Q9SH-4N2B

   Task-Id: 169040e6-a9e0-4891-83fa-7b7c943ea38d
   Message:    Device claimed successfully
   Claim Id:   d1ab5aa2-2a00-40a6-e634-08dee67a1dd3
   Expires At: 2026-07-21T12:26:30.222Z

This does not pull in a device directly. What it does is register the token in
the appstore within your tenant. The device, having generated that token, waits
to register until the store recognizes it. As long as you claim the token within
its validity window (see ``Expires At``), the device is then allowed to complete
registration and is bound to your tenant.

List your devices
~~~~~~~~~~~~~~~~~

.. code:: console

   host:~$ m2cp device list

   Serial                                  Type           Arch     Name           Store Activity    Messaging Activity    Online    Model                Uplink Mode
   7bae3a29-a7b8-584e-995d-330f958aec46    Edge Device    ARM64    n/a            2026-07-20        2026-07-20            false     generic-arm64 (1)    SIGNALR_HUB
   73fe2304-6be9-5f4a-8086-bffcbe38f930    Edge Device    ARM64    demo-device    2026-07-21        2026-07-21            true      generic-arm64 (1)    SIGNALR_HUB

A freshly claimed device shows up with ``Name: n/a`` and ``Online: true`` once
it checks in.

Rename the device
~~~~~~~~~~~~~~~~~

Give it something memorable with ``modify -n/--name`` (the name must be unique
within your tenant):

.. code:: console

   host:~$ m2cp device modify 73fe2304-6be9-5f4a-8086-bffcbe38f930 --name demo-device

   Task-Id: f02a003b-e89e-451f-ab4d-aa989853634a
   Message: Device '73fe2304-6be9-5f4a-8086-bffcbe38f930': active=true, name='demo-device', description='n/a'

``modify`` also carries:

+-----------------------------------+-----------------------------------+
| Flag                              | Purpose                           |
+===================================+===================================+
| ``-n, --name``                    | Set a new (tenant-unique) name    |
+-----------------------------------+-----------------------------------+
| ``-d, --description``             | Set a free-text description       |
+-----------------------------------+-----------------------------------+
| ``--device-activated yes|no``     | Activate / deactivate. A          |
|                                   | **deactivated device is denied    |
|                                   | communication with the server**   |
+-----------------------------------+-----------------------------------+

Inspect a device
~~~~~~~~~~~~~~~~

``device info`` is your at-a-glance dashboard for a single device: identity,
live gateway stats, deployment group, installed software, and pending actions:

.. code:: console

   host:~$ m2cp device info demo-device

   Device:
     ├─ Id:                      bce20e06-f0b8-4fd2-2adb-08dee67a3378
     ├─ OS Serial:               73fe2304-6be9-5f4a-8086-bffcbe38f930
     ├─ Name:                    demo-device
     ├─ Last Messaging Mode:     SIGNALR_HUB
     ├─ Last Uptime:             1m 48s
     ├─ Type:                    Edge Device
     ├─ Architecture:            ARM64
     ├─ Model Name:              generic-arm64
     └─ Model Revision:          1

   Gateway Stats:
     ├─ Heartbeat Counter:       10
     ├─ Uptime Seconds:          108
     ├─ Message Hub Reachable:   yes
     ├─ System CPU Usage:        2%
     ├─ FS Free MB:              955
     └─ Gateway Mem Usage MB:    27

   Deployment Group:
     ├─ Name:           demo-dgroup
     └─ Owner:          PhyHUB Operator (phyhub.operator@phyhub.com)

   Installed Apps:
   System    Name                Version     Revision    Description
   -         core24              1.3.3       1           The base snap based on the Ubuntu 24.04 release.
   -         m2cp-gateway        3.4.0       7           This snap provides the gateway to the cloud.
   yes       snapd               5.1.0.55    14          Install, configure, refresh and remove snap packages.

   Installed Image:
   Name                 Architecture    Version       Revision    Rating          Rating Description
   phytec-liot-image    arm64           2026-07-23    16          Stable          Demo Image

   Pending Actions:
   * No pending actions

For live troubleshooting, ``device logs`` and other hands-on commands are
covered in `Part 7 <#part-7-operating-a-device-directly>`__.

--------------

Part 2: Publishing Software & Building Images
---------------------------------------------

The following commands are for developers who produce software rather than just
deploy it.

Uploading software
~~~~~~~~~~~~~~~~~~

Apps and OS images are both uploaded with the same command (store ≥ 5.3.0):

.. code:: console

   host:~$ m2cp store software push <upload.tar> "<version description>"

   Initiating upload for '.../phytec-liot-image_2026-07-23_upload.tar'
   Uploading 769515520 bytes (upload id 019f820a3721757aa6e86b829bdeac75)

The quoted string is the **version/upload description**. A freshly pushed
revision lands **Unrated** and cannot be deployed until a **software manager**
rates it (see `Part 4 <#part-4-software-ratings>`__). Inspect the catalog
afterwards with ``m2cp store app list`` (add ``--json`` for scripting).

The ``upload.tar`` is not just the raw ``.snap`` or image: it has a required
structure and must contain a ``software.yaml`` manifest. See `Part 3
<#part-3-packaging-software-for-upload>`__ for how to package an app or an
image. Once uploaded and rated, software is added to a deployment group like any
other (``store dgroup software add <dgroup> <software> <version>``).

Push a model
~~~~~~~~~~~~

A **model** describes a device type and the snaps it ships with. Push a model
definition (a JSON file) with a message:

.. code:: console

   host:~$ m2cp store model push ./model-phyboard-segin-imx93-2.json "Initial model"

If a model of that name already exists, the store refuses a plain push::

   Error: graphql: Model with this name is already pushed. Use update flag to push a new revision.

Add the update flag to publish a **new revision** of an existing model.

A model JSON looks like this (IDs are filled in by the store on push):

.. code:: json

   {
       "type": "model",
       "series": "16",
       "brand-id": "PLACEHOLDER",
       "model": "phyboard-pollux-imx8mp-3",
       "classic": "true",
       "architecture": "arm64",
       "snaps": [
           { "name": "snapd",            "type": "snapd", "default-channel": "latest/stable" },
           { "name": "core24",           "type": "base",  "default-channel": "latest/stable" },
           { "name": "m2cp-gateway",     "type": "app",   "default-channel": "latest/stable" },
           { "name": "m2cp-message-hub", "type": "app",   "default-channel": "latest/stable" },
           { "name": "edge-ota-rauc",    "type": "app",   "default-channel": "latest/stable" }
       ]
   }

Create a seed (required for building a custom image)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A **seed** is the set of snaps plus the model that get baked into a custom OS
image at build time. Generate the seed structure from a seed YAML with ``m2cp
store system snapd-seed generate``, passing the YAML and an output directory:

.. code:: console

   host:~$ m2cp store system snapd-seed generate ./seed-phyboard-segin-imx93-2.yaml seed-phyboard-segin-imx93-2

   Skipping download of seed-phyboard-segin-imx93-2/seed/snaps/snapd_14.snap as it already exists
   Skipping download of seed-phyboard-segin-imx93-2/seed/snaps/m2cp-gateway_7.snap as it already exists
   Skipping download of seed-phyboard-segin-imx93-2/seed/snaps/core24_1.snap as it already exists
   Seed structure created at: seed-phyboard-segin-imx93-2/seed

The command downloads each snap named in the seed (skipping any already present)
and assembles the ``seed/`` directory your image builder consumes.

A seed YAML pins the store, the model + revision, and the exact snap versions:

.. code:: yaml

   store:
     url: https://api.phyhub.phytec.de/graphql
   model:
     name: phyboard-pollux-imx8mp-3
     revision: 1
   snaps:
   - name: snapd
     arch: arm64
     version: 5.1.0.55
   - name: m2cp-gateway
     arch: arm64
     version: 3.4.0
   - name: m2cp-message-hub
     arch: arm64
     version: 4.5.18
   - name: core24
     arch: arm64
     version: 1.3.3
   - name: edge-ota-rauc
     arch: arm64
     version: 0.5.1

Feed the resulting ``seed/`` directory into your Yocto / image build to produce
a device image that boots pre-loaded with exactly these snaps and this model.

--------------

Part 3: Packaging Software for Upload
-------------------------------------

Before you can ``store software push`` (see `Part 2
<#part-2-publishing-software--building-images>`__), the artifacts have to be
packaged into an ``upload.tar`` with the structure below. This is the same
format for apps and images; only the files inside ``artifact/`` differ.

The upload structure
~~~~~~~~~~~~~~~~~~~~

Every upload is a ``.tar`` archive with a fixed layout::

   upload.tar
     artifact/
       software.yaml      # required manifest (see below)
       <artifact files>   # the .snap, image, and/or RAUC bundle
     sbom/                # optional SBOM documents (stored, never sent to devices)

-  The archive’s file name does not matter (``upload.tar`` here is just a
   placeholder); only its contents are read.
-  ``artifact/`` and ``artifact/software.yaml`` are **required**.
-  The other files in ``artifact/`` depend on what you package (snap vs. image);
   see below. File roles are determined by **extension**, not by file name.
-  ``sbom/`` is optional.

The ``software.yaml`` manifest
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``software.yaml`` is the manifest the backend reads to identify the revision and
to decide how to handle the rest of ``artifact/``. Common fields:

+-----------------------+-----------------------+-----------------------+
| Field                 | Required for          | Description           |
+=======================+=======================+=======================+
| ``format-version``    | all                   | Manifest format       |
|                       |                       | version. Currently    |
|                       |                       | ``3``.                |
+-----------------------+-----------------------+-----------------------+
| ``category``          | all                   | ``app`` or ``image``. |
+-----------------------+-----------------------+-----------------------+
| ``class``             | app, image            | Class within the      |
|                       |                       | category (``snap``    |
|                       |                       | for apps, ``yocto``   |
|                       |                       | for images).          |
+-----------------------+-----------------------+-----------------------+
| ``update-mechanism``  | image                 | OTA mechanism.        |
|                       |                       | ``rauc`` for images.  |
+-----------------------+-----------------------+-----------------------+
| ``software-name``     | all                   | Software name.        |
|                       |                       | Matches the name used |
|                       |                       | in update actions and |
|                       |                       | refresh requests.     |
+-----------------------+-----------------------+-----------------------+
| ``software-version``  | all                   | Software version.     |
+-----------------------+-----------------------+-----------------------+
| ``summary``           | image                 | Short description of  |
|                       |                       | the software.         |
+-----------------------+-----------------------+-----------------------+
| ``architecture``      | image                 | Target CPU            |
|                       |                       | architecture          |
|                       |                       | (``arm32``,           |
|                       |                       | ``arm64``, ``amd64``, |
|                       |                       | …).                   |
+-----------------------+-----------------------+-----------------------+
| ``device-model``      | image                 | Target device model   |
|                       |                       | name as registered in |
|                       |                       | the store.            |
+-----------------------+-----------------------+-----------------------+

Optional fields: ``device-model-version`` (restrict the artifact to one model
version) and a ``build:`` block (``commit``, ``upstream-version``, ``datetime``)
for provenance.

The **revision identity** is the combination of ``software-name``,
``software-version``, ``class``, and, for images, ``update-mechanism``,
``device-model``, and ``device-model-version``. If an upload’s identity matches
an existing revision it extends that revision; otherwise it creates a new one.

Packaging an app (snap)
~~~~~~~~~~~~~~~~~~~~~~~

For an app, ``artifact/`` holds ``software.yaml`` and exactly one ``.snap``
file::

   upload.tar
     artifact/
       software.yaml
       <any-name>.snap

The snap manifest is minimal. The backend extracts the rest (summary,
architecture, base, confinement, ...) from ``meta/snap.yaml`` inside the
``.snap``:

.. code:: yaml

   format-version: 3
   category: app
   class: snap
   software-name: edge-ota-rauc
   software-version: 0.5.3

``software-name`` and ``software-version`` MUST match ``name`` and ``version``
in the snap's ``meta/snap.yaml``, otherwise the upload is rejected.

Packaging an image (Yocto + RAUC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For an OS image, ``artifact/`` holds ``software.yaml`` plus a provisioning image
and a RAUC bundle::

   upload.tar
     artifact/
       software.yaml
       <any-name>.<wic|img|partup>   # provisioning image, flashed onto a fresh device
       <any-name>.raucb              # RAUC bundle, the OTA update deliverable

The provisioning image (``.wic`` / ``.img`` / ``.partup``) is used to flash new
devices; the ``.raucb`` bundle is what devices download for OTA updates.

.. note::
   An image upload currently requires **both** files in the same ``upload.tar``:
   the provisioning image **and** the RAUC bundle.

The image manifest carries the full common fields:

.. code:: yaml

   format-version: 3
   category: image
   class: yocto
   update-mechanism: rauc
   software-name: phytec-liot-image
   software-version: "2026-07-23"
   summary: "PHYTEC L-IoT image for phyboard-pollux imx8mp"
   architecture: arm64
   device-model: generic-arm64

With the ``upload.tar`` built, publish it as shown in `Part 2
<#part-2-publishing-software--building-images>`__.

--------------

Part 4: Software Ratings
------------------------

Every software version carries a rating that gates deployment. This is identical
to the UI's approval model:

+-----------------------+-----------------------+-----------------------+
| Rating                | Deployable?           | Meaning               |
+=======================+=======================+=======================+
| **Unrated**           | No                    | Freshly uploaded, not |
|                       |                       | yet reviewed          |
+-----------------------+-----------------------+-----------------------+
| **Experimental**      | Yes                   | Early-stage /         |
|                       |                       | developer build       |
+-----------------------+-----------------------+-----------------------+
| **Edge**              | Yes                   | Field-ready, not      |
|                       |                       | fully                 |
|                       |                       | production-validated  |
+-----------------------+-----------------------+-----------------------+
| **Stable**            | Yes                   | Fully validated,      |
|                       |                       | production-ready      |
+-----------------------+-----------------------+-----------------------+
| **Denied**            | No                    | Rejected              |
+-----------------------+-----------------------+-----------------------+
| **Deprecated**        | No                    | Retired / superseded; |
|                       |                       | no longer for new     |
|                       |                       | deployments           |
+-----------------------+-----------------------+-----------------------+

Ratings are assigned **after** upload by a **software manager**, not by whoever
uploads the software. A freshly uploaded version stays **Unrated** until a
software manager reviews it and gives it a rating. Ratings can also be changed
later as a version is re-evaluated (for example, downgraded once it turns out to
be broken). Ratings and their descriptions are visible in ``store dgroup info``
and ``device info`` output (the ``Rating`` / ``Rating Description`` columns).

Reviewing and setting ratings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A software manager reviews the queue and sets ratings from the CLI with ``store
software rate``.

List software by rating (defaults to **Unrated**, i.e. the review queue):

.. code:: console

   host:~$ m2cp store software rate list

   Task-Id: eb1b018f-83e7-4353-9a8c-cf9ba2a86860
   Software                Architecture    Version             Rating     Uploaded            Developer Note
   snapd                   arm64           5.1.0.0-dev1 (7)    Unrated    2026-07-04 21:34    Fix recovery on full system upgrade
   test-firmware-upload    arm32           3.3.0 (1)           Unrated    2026-07-16 07:20    Test

The **Developer Note** column is the version/upload description the uploader
supplied at push time.

Set a rating with ``rate set``. It takes five arguments, ``<softwareName>
<architecture> <revision> <rating> <description>``:

.. code:: console

   host:~$ m2cp store software rate set snapd arm64 7 Deprecated "Outdated"

   Rating of software snapd (ARM64) version 5.1.0.0-dev1 (7) updated to Deprecated

The final ``description`` becomes the **Rating Description**.

.. note::
   The ``<revision>`` argument is the numeric revision (e.g. ``7``), not the
   version string (``5.1.0.0-dev1``). Passing a version currently fails with
   ``invalid software revision``. Support for addressing by version is coming.

--------------

Part 5: Deployment Groups
-------------------------

A deployment group holds a target set of software. Add a device to the group and
it installs that software automatically.

Create a group
~~~~~~~~~~~~~~

Create a group for a given model. The model form takes ``<modelType> <modelName>
<modelRevision>``:

.. code:: console

   host:~$ m2cp store dgroup create demo-dgroup m2cp generic-arm64 1

   Task-Id: 586e2e3a-b033-43f0-a40f-06756889d045
   Deployment Group created from model

``m2cp store dgroup create`` accepts a few forms of the second argument:

+-----------------------------------+---------------------------------------------+
| Form                              | Arguments after the name                    |
+===================================+=============================================+
| From a model triple               | ``<modelType> <modelName> <modelRevision>`` |
|                                   | (as above)                                  |
+-----------------------------------+---------------------------------------------+
| From an existing device           | ``<deviceName \| osSerial>``                |
+-----------------------------------+---------------------------------------------+

Creating a group **from a device** is a handy shortcut: instead of listing
software by hand, the group inherits the device’s model *and* seeds its target
set from that device’s current install state as known to the store. In other
words, the software already reported on that device becomes the group’s target.
You can then adjust it with ``software add`` / ``software modify`` as usual.

.. code:: console

   host:~$ m2cp store dgroup create demo-dgroup demo-device

.. note::
   **The OS image is not assigned automatically.** When a group is created
   (including from a device), its target set does not include the image. The
   appstore still *detects* the image already present on a device and reports
   it, but it is not part of the group’s target. So whenever you want to update
   or change the image, you must **add it to the group first** with ``store
   dgroup software add`` (see below); only then will the change be rolled out.

Optional flag: ``-d/--description`` sets a description for the group.

List and inspect groups
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

   host:~$ m2cp store dgroup list
   host:~$ m2cp store dgroup info demo-dgroup

``info`` shows the group’s model, owner, pending-action count, its
member **Devices**, and the target **Software (App)** table::

   Deployment Group
       ├── Id:              37249cad-f0e8-40f4-7940-08dee67a49bd
       ├── Name:            demo-dgroup
       ├── Model
       │   ├── Type:            Edge Device
       │   ├── Name:            generic-arm64
       │   └── Revision:        1
       ├── Owner:           PhyHUB Operator (phyhub.operator@phyhub.com)
       └── Pending Actions: 1

   Devices
   Serial                                  Name           Pending Actions
   73fe2304-6be9-5f4a-8086-bffcbe38f930    demo-device    0

   Software (App)
   Core    Name                Version          Rating          Version Description
   -       core24              1.3.3 (1)        Stable          republish core24
   -       m2cp-gateway        3.4.0 (7)        Stable          Release 3.4.0 with updated D-Bus interfaces
   yes     snapd               5.1.0.55 (14)    Edge            OTA support, Yocto adjustments

Add software to the group
~~~~~~~~~~~~~~~~~~~~~~~~~

Add a software version to the group’s target set. The third argument is the
software ``version`` (or the literal ``latest`` for the newest):

.. code:: console

   # Add an app by version
   host:~$ m2cp store dgroup software add demo-dgroup hello-world 6.4.2

   # Add the OS image the same way
   host:~$ m2cp store dgroup software add demo-dgroup phytec-liot-image 2026-07-23

::

   Task-Id: e61bcd50-e7f4-46a3-a280-66db24d09727
   Software added to Deployment Group

To move the group to a different version later, use ``software modify`` (not
``add``):

.. code:: console

   host:~$ m2cp store dgroup software modify demo-dgroup phytec-liot-image 2026-07-24

   Task-Id: 3ed0f7e4-956e-4155-b430-35a2193dc2d8
   Software revision modified in Deployment Group

Remove software from the group with ``m2cp store dgroup software remove <dgroup>
<software>``.

.. note::
   Only rated software (**Experimental**, **Edge**, **Stable**) can be added.
   **Unrated** and **Denied** versions are rejected. See `Part 3
   <#part-3-software-ratings>`__.

Add the device to the group
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the step that actually triggers installs. Assign the device to the
group:

.. code:: console

   host:~$ m2cp device dgroup set demo-device demo-dgroup

   Task-Id: fe8242d4-333e-4b34-9ec2-6d5046843cdf
   assigned Device 73fe2304-6be9-5f4a-8086-bffcbe38f930 (demo-device) to Deployment Group 37249cad-f0e8-40f4-7940-08dee67a49bd (demo-dgroup)

The backend now calculates update actions and pushes the group's software to the
device. If you ever need to take the device back out of the group, you can do so
with ``m2cp device dgroup unset <device>``.

.. note::
   **A device belongs to at most one deployment group.** To change what it runs,
   edit its current group’s software or ``set`` it to a different group.

Right after assignment, ``device info`` will show the incoming work under
**Pending Actions**::

   Pending Actions:
   Action     App            Current    Target       Download    Delta
   Install    hello-world    - (-)      6.4.2 (2)    20.0KB      n/a

.. note::
   **Pending Actions** is the legacy way of showing outstanding updates for a
   device. A transition to the new **update actions** (see `Part 6
   <#part-6-update-actions>`__) is in progress, so you will see both for now.
   Update actions are more powerful: they carry a **state** and allow
   **fine-grained, per-action logs**.

Part 6: Update Actions
----------------------

An **update action** is one calculated change for a device: install an app,
update an app, update the OS image, or delete something. This is where you watch
software actually land.

List update actions for a device
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: console

   host:~$ m2cp device update list demo-device

   Id                                      Software         Category    Type          Started                Current         Target      Status
   87b8af98-9d67-4d9a-8b7c-08dee67a5523    hello-world      App         INSTALLING    2026-07-21 10:02:04    -               6.4.2       SUCCEEDED
   93fd869e-5f36-4778-8b79-08dee67a5523    snapd            App         UPDATING      2026-07-21 09:56:54    5.1.0.0-dev7    5.1.0.55    SUCCEEDED
   02777d97-540b-44e0-8b7b-08dee67a5523    m2cp-gateway     App         UPDATING      2026-07-21 09:56:54    3.3.11          3.4.0       SUCCEEDED

If a device has no work queued you'll simply see ``No update actions found``.

Inspect one action
~~~~~~~~~~~~~~~~~~

Pass an action Id to ``update info`` for the full phase-by-phase trace:

.. code:: console

   host:~$ m2cp device update info 87b8af98-9d67-4d9a-8b7c-08dee67a5523

   Id:        87b8af98-9d67-4d9a-8b7c-08dee67a5523
   Software:  hello-world (arm64)
   Type:      INSTALLING
   Current:   -
   Target:    6.4.2
   Status:    SUCCEEDED

   Timestamp              Component    Phase          Mechanism    Status      Message
   2026-07-21 10:02:04    BACKEND      PREPARATION                 Done        New update action calculated
   2026-07-21 10:02:19    TARGET       DOWNLOAD       SNAP         Progress    Download snap "hello-world" (2) from channel "stable"
   2026-07-21 10:02:22    TARGET       INSTALL        SNAP         Progress    Mount snap "hello-world" (2)
   2026-07-21 10:02:35    TARGET       ACTIVATE       SNAP         Done        Make snap "hello-world" (2) available to the system
   2026-07-21 10:02:39    TARGET       ACTIVATE       SNAP         Done        Run health check of "hello-world" snap

In the trace, the **Component** column shows where each step ran, one of
``BACKEND`` (the store), ``PROXY`` (the device's update proxy), or ``TARGET``
(the device itself).

Follow an update live
~~~~~~~~~~~~~~~~~~~~~

``update follow`` opens a live TUI that refreshes as the device reports
progress. It is the best way to watch an OS image roll out:

.. note::
   ``update follow`` is not available in ``--json`` mode. It is a development
   and debugging aid, not a command intended for automation. For scripting, use
   ``update list`` / ``update info`` instead.

.. code-block:: console

   # Follow all active actions for a device
   host:~$ m2cp device update follow demo-device

   # Or follow a single action by Id
   host:~$ m2cp device update follow fd37b08c-21e8-469f-8b7d-08dee67a5523

.. code-block:: console

   host:~$ m2cp follow  update action fd37b08c  ·  updated just now

   ▸ Details — phytec-liot-image · started 32s ago
   Type     UPDATING
   Status   ▶ IN_PROGRESS
   Version  2026-07-23 → 2026-07-24
   When     Component  Phase            Mechanism  Status    Message
   25s ago  PROXY      ACTION_RECEIVED  RAUC       Done      Successfully received update action
   24s ago  TARGET     INSTALL          RAUC       Progress  installation progress: 42% Copying image to rootfs.1
   ...
   ↑/↓ scroll · r refresh · q quit

Press ``r`` to force a refresh and ``q`` to quit. An OS-image update finishes
with a reboot::

   2026-07-21 10:13:31    TARGET    INSTALL     RAUC    Done        installation of artifact completed successfully
   2026-07-21 10:13:31    PROXY     ACTIVATE    RAUC    Progress    refresh cycle completed successfully, rebooting system

After the reboot, ``device info`` shows the new ``Installed Image`` version and
``Pending Actions: * No pending actions``.

Installation history
~~~~~~~~~~~~~~~~~~~~

For the full record of past installs, updates, and removals on a device:

.. code-block:: console

   host:~$ m2cp device history demo-device

Triggering a refresh
~~~~~~~~~~~~~~~~~~~~

A device checks in on its own schedule, and the backend also triggers a refresh
automatically once whenever a device is online or comes online. To make it look
for and apply outstanding updates right now, send it a refresh trigger:

.. code-block:: console

   host:~$ m2cp device update trigger do demo-device

To see the triggers sent to a device, whether the device actually received them,
and any that are still scheduled, use ``trigger history``:

.. code-block:: console

   host:~$ m2cp device update trigger history demo-device

   Task-Id: 505c9976-ce04-4ac4-814a-97cfada36d22
   Created                Command              Status     Expires At             Responded At           Id
   2026-07-21 10:36:43    TriggerRefresh       Success    2026-07-21 10:36:43    2026-07-21 10:36:43    c4bc4bb4-6fb6-4551-8730-08dee67a8a99
   2026-07-21 10:04:35    TriggerRefresh       Success    2026-07-21 10:04:36    2026-07-21 10:04:36    722b4820-000d-4ac9-872f-08dee67a8a99
   2026-07-21 10:02:09    DeviceSnapRefresh    Expired    2026-07-21 10:02:39    -                      0f03a8bc-19a6-459a-872e-08dee67a8a99
   2026-07-21 09:57:31    DeviceSnapRefresh    Expired    2026-07-21 09:58:01    -                      a48385b9-e6a3-4f53-872d-08dee67a8a99
   2026-07-21 09:56:59    DeviceSnapRefresh    Expired    2026-07-21 09:57:29    -                      e4efa59b-f0b2-4cd5-872c-08dee67a8a99

Each row is a trigger the store sent to the device. The **Status** column tells
you whether the device picked it up: ``Success`` means the device received and
responded to it (see **Responded At**), while ``Expired`` means it was not
collected before its **Expires At** time, i.e. the device never received it
because the request timed out.

--------------

Part 7: Operating a Device Directly
-----------------------------------

Beyond updates, the ``device`` tree gives you hands-on access, handy during
bring-up and debugging:

+-----------------------------------+-----------------------------------+
| Command                           | What it does                      |
+===================================+===================================+
| ``m2cp device logs <device>``     | Fetch / stream logs from the      |
|                                   | device                            |
+-----------------------------------+-----------------------------------+
| ``m2cp device reboot <device>``   | Reboot the device                 |
+-----------------------------------+-----------------------------------+
| ``m2cp device ping <address>``    | Ping an m2cp address and report   |
|                                   | the reached node’s uptime         |
+-----------------------------------+-----------------------------------+

--------------

Putting It All Together: A Typical CLI Workflow
-----------------------------------------------

+--------+------------------------------------------------------------------------+
| Step   | Command                                                                |
+========+========================================================================+
| 1      | Provision the device on the hardware; note its **claiming token**      |
+--------+------------------------------------------------------------------------+
| 2      | ``m2cp user login --store <url> --method browser``                     |
+--------+------------------------------------------------------------------------+
| 3      | ``m2cp device claim <token>``                                          |
+--------+------------------------------------------------------------------------+
| 4      | ``m2cp device modify <serial> --name <name>``                          |
+--------+------------------------------------------------------------------------+
| 5      | ``m2cp store dgroup create <name> <modelType> <modelName> <revision>`` |
+--------+------------------------------------------------------------------------+
| 6      | ``m2cp store dgroup software add <dgroup> <software> <version>``       |
+--------+------------------------------------------------------------------------+
| 7      | ``m2cp device dgroup set <device> <dgroup>``                           |
+--------+------------------------------------------------------------------------+
| 8      | ``m2cp device update follow <device>`` (watch installs land)           |
+--------+------------------------------------------------------------------------+
| 9      | ``m2cp device info <device>`` (confirm installed software)             |
+--------+------------------------------------------------------------------------+

Developer / publishing steps, as needed:

+-----------------------------------+-------------------------------------------------------------------+
| Task                              | Command                                                           |
+===================================+===================================================================+
| Package an app or image           | Build an ``upload.tar`` (see `Part                                |
|                                   | 3 <#part-3-packaging-software-for-upload>`__)                     |
+-----------------------------------+-------------------------------------------------------------------+
| Publish software (app/image)      | ``m2cp store software push <upload.tar> "<version desc>"``        |
+-----------------------------------+-------------------------------------------------------------------+
| Push a model                      | ``m2cp store model push ./<model>.json "<msg>"``                  |
+-----------------------------------+-------------------------------------------------------------------+
| Create a seed                     | ``m2cp store system snapd-seed generate ./<seed>.yaml <out-dir>`` |
+-----------------------------------+-------------------------------------------------------------------+

--------------

Frequently Asked Questions
--------------------------

How do I address a device, by serial or by name?
   Either, every ``device`` subcommand accepts the OS-Serial (the UUID) or the
   friendly name you set with ``modify --name``. Names must be unique within
   your tenant.

Can I get machine-readable output?
   Yes. Append ``--json`` to any command and pipe it into ``jq``.

What’s the difference between ``store dgroup software add`` and ``modify``?
   ``add`` puts a software version into a group that doesn’t have it yet;
   ``modify`` changes the target version of software already in the group. Using
   ``add`` on something already present is an error.

A device can be in more than one deployment group, right?
   No. Exactly one at a time. Use ``device dgroup set`` to move it or ``device
   dgroup unset`` to remove it.

How do I trigger an update check manually?
   ``m2cp device update trigger do <device>``.
