UI Manual: Devices, Software & Assets
=====================================

This guide walks you through everything you need to do in the phyHUB web
interface to get your IoT devices up and running -- from registering a device
for the first time to installing software on it and linking it to a piece of
physical equipment.

--------------

How Everything Connects — The Big Picture
-----------------------------------------

phyHUB manages three things at once: **devices**, **software**, and **physical
assets**. Before diving into the steps, it helps to understand how these pieces
relate to each other.

::

   BEFORE THE UI
   ────────────────────────────────────────────────────────
     Physical device  →  Provisioned via terminal
                          (see Device Provisioning Manual)

   IN THE phyHUB UI
   ────────────────────────────────────────────────────────
     Device registered
          │
          ├──▶  Added to a Deployment Group
          │           │
          │           └──▶  Apps installed automatically
          │
          └──▶  Commissioned to an Asset
                      │
                      └──▶  Linked to physical equipment
                             (pump, robot arm, CNC machine…)

Here is what each of these concepts means in plain language:

+-----------------------------------+-----------------------------------+
| Concept                           | What it is                        |
+===================================+===================================+
| **Device**                        | A physical edge device (e.g., a   |
|                                   | Raspberry Pi or industrial        |
|                                   | gateway) attached to a piece of   |
|                                   | equipment                         |
+-----------------------------------+-----------------------------------+
| **App / Application**             | Software that runs on a device —  |
|                                   | uploaded to the phyHUB store and  |
|                                   | deployed remotely                 |
+-----------------------------------+-----------------------------------+
| **Deployment Group**              | A named group of devices that     |
|                                   | share the same set of apps.       |
|                                   | Assigning a device to a group     |
|                                   | automatically installs the        |
|                                   | group’s apps on it                |
+-----------------------------------+-----------------------------------+
| **Asset**                         | A physical piece of industrial    |
|                                   | equipment (pump, motor, conveyor  |
|                                   | belt, etc.) that one or more      |
|                                   | devices are attached to           |
+-----------------------------------+-----------------------------------+
| **Asset Hierarchy**               | A template that describes what    |
|                                   | devices an asset needs and how    |
|                                   | they are organized — defined      |
|                                   | before any real devices are       |
|                                   | assigned                          |
+-----------------------------------+-----------------------------------+
| **Commissioning**                 | The final step: assigning a       |
|                                   | specific physical device          |
|                                   | (identified by its serial number) |
|                                   | to a slot in an asset’s hierarchy |
+-----------------------------------+-----------------------------------+
| **Attribute Set**                 | A set of custom data fields you   |
|                                   | can attach to an asset type to    |
|                                   | record extra information (e.g.,   |
|                                   | installation date, manufacturer,  |
|                                   | location)                         |
+-----------------------------------+-----------------------------------+

--------------

Before You Begin:
-----------------

1. User Management

   **This step happens before you open the phyHUB UI.**

   Before you can interact with the web UI, you have to first set up and manage
   your team's access to phyHUB.

   This means creating your organization, inviting colleagues, assigning the
   right roles.

   Please check the **User Management Manual** found in the same folder as this
   guide. Once your organization is fully setup and you have invited all your
   team memebrs, you can proceed with the rest of this manual.

2. Provisioning Your Device

   **This step happens before you open the phyHUB UI.**

   Every physical device must be provisioned -- enrolled with the platform’s
   identity system -- before it can be registered through the web interface.
   This involves running a set of commands on the device itself (or during
   manufacturing).

   Full instructions are provided in the **Device Provisioning Manual (using the
   terminal)** found in the same folder as this guide. Complete that process
   first, then return here to continue with the UI steps.

3. The phyHUB web UI

After completing steps 1 and 2, you now have devices that are ready to be
activated and users that can perform meaningful actions with them in the store.

Head to https://www.phyhub.phytec.de/ and begin your journey.

--------------

Part 1: Onboarding Your Devices
-------------------------------

Once a device has been provisioned, you register it in phyHUB so the platform
knows it exists and can manage it.

The Device List
~~~~~~~~~~~~~~~

Navigate to the **Devices** section in the left sidebar. You will see a table
listing all registered devices with the following information for each:

+-----------------------------------+-----------------------------------+
| Column                            | What it shows                     |
+===================================+===================================+
| **Serial Number**                 | The unique hardware identifier of |
|                                   | the device                        |
+-----------------------------------+-----------------------------------+
| **Model**                         | The device model (e.g., a         |
|                                   | specific type of gateway or       |
|                                   | controller)                       |
+-----------------------------------+-----------------------------------+
| **Status**                        | Whether the device is Active,     |
|                                   | Offline, or Pending activation    |
+-----------------------------------+-----------------------------------+
| **Last Seen**                     | When the device last communicated |
|                                   | with the platform                 |
+-----------------------------------+-----------------------------------+
| **Deployment Group**              | Which deployment group (if any)   |
|                                   | this device is currently in       |
+-----------------------------------+-----------------------------------+

Registering a New Device
~~~~~~~~~~~~~~~~~~~~~~~~

1. Click the **Activate Device** button at the top of the page.
2. Enter the **device token** you obtained from the device during the terminal
   provisioning step.
3. Click **Save**. The device will appear in the list in a few moments if the
   activation process was successful.

The Device Details Page
~~~~~~~~~~~~~~~~~~~~~~~

Click on any device in the list to open its details page. Here you will find
several tabs:

+-----------------------------------+-----------------------------------+
| Tab                               | What it shows                     |
+===================================+===================================+
| **Details**                       | Serial number, model, current     |
|                                   | status, and assigned deployment   |
|                                   | group                             |
+-----------------------------------+-----------------------------------+
| **Software**                      | The current installation state of |
|                                   | each app on the device            |
+-----------------------------------+-----------------------------------+
| **Logs**                          | Live and recent log output from   |
|                                   | the device — useful for           |
|                                   | troubleshooting                   |
+-----------------------------------+-----------------------------------+

--------------

Part 2: Uploading Applications to the Store
-------------------------------------------

phyHUB works like an app store: developers upload application packages via the
terminal, a reviewer then rates them through the UI, and once rated the apps
become available to be assigned to deployment groups and pushed to devices.

How the App Approval Process Works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   App uploaded via terminal  →  Status: "Unrated"
                                      │
                           Software Manager reviews it
                                      │
                 Approved  ──▶  "Experimental", "Edge", or "Stable"
                                 All three are available in deployment groups

                 Rejected  ──▶  "Denied"  (not available for deployment)

Apps with a status of **Experimental**, **Edge**, or **Stable** are all visible
in the deployment group app selector and can be assigned to devices. Apps that
are **Unrated** or **Denied** cannot be added to any deployment group.

Reviewing and Rating Apps (Software Manager)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your role is **Software Manager** or **Software Admin**, you are responsible
for reviewing apps uploaded to the store and setting their status. Apps are
uploaded via the terminal by developers and will initially appear with
**Unrated** status.

1. Open the **Software Review** section, click on the **Apps Pending Review**
   tab and find the app you want to review.
2. Click on the app to open its details.
3. Check the app information and package.
4. Use the **Status** dropdown to change the rating:

   - **Experimental** → available for deployment; indicates an early-stage or
     developer build
   - **Edge** → available for deployment; indicates a field-ready but not fully
     production-validated release
   - **Stable** → available for deployment; indicates a fully validated,
     production-ready release
   - **Denied** → not available for deployment; the app has been rejected

5. Save your changes. The developer will see the updated status on their app.

--------------

Part 3: Creating Deployment Groups
----------------------------------

A deployment group is how phyHUB knows which apps to install on which devices.
Instead of assigning apps to individual devices, you define a group for a
specific device model and list the apps it should run. Any device added to that
group will automatically receive those apps.

Creating a New Group
~~~~~~~~~~~~~~~~~~~~

1. Go to the **Devices** section in the left sidebar and then click on the
   **Deploymnet Groups** tab.
2. Click **Create Group**.
3. Enter a **name** for the group (e.g., ``production-pump-controllers``).
4. Select the **device model** -- only devices of this model type can be added to
   the group.
5. Optionally add a **description**.
6. Click **Save**.

Adding Apps to the Group
~~~~~~~~~~~~~~~~~~~~~~~~

1. Open the deployment group you just created.
2. Click the **Apps** tab.
3. Click **Add Application**.
4. Select the app and the specific **version** (revision) you want deployed.
   Apps with **Unrated** or **Denied** status do not appear here -- only apps
   rated as **Experimental**, **Edge**, or **Stable** are available.
5. Click **Add**. The app is now part of this group’s target configuration.

You can add multiple apps to a single group. All devices in the group
will receive all the listed apps.

Adding Devices to the Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. In the same deployment group, click the **Devices** tab.
2. Click **Add Devices**.
3. Select one or more from the list of available devices matching the group's
   device model.
4. Click **Add**.

Once a device is added to a group, phyHUB will begin pushing the group's
applications to it automatically. You can monitor the installation progress from
the device's details page.

.. note::
   A device can only belong to one deployment group at a time. If you need to
   change which apps a device runs, either update the apps in its current group
   or move it to a different group.

--------------

Part 4: Setting Up Your Asset Hierarchy
---------------------------------------

An **asset** in phyHUB represents a physical piece of industrial equipment -- a
pump, a motor, a robotic arm, a CNC machine. Linking your devices to assets lets
you see not just *which* device has a problem, but *which piece of equipment* it
belongs to.

Asset management involves three layers, built in order::

   Asset Type   →   Asset Model (with hierarchy)   →   Asset Instance
     "Pump"           "Model XYZ-500 Pump"              "Pump 001, Hall B"
                       (defines which devices           (a real machine)
                        it needs and how they
                        are organized)

Step 1: Create an Asset Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An **Asset Type** is the broadest category -- it describes a class of equipment,
not a specific product.

1. Go to the **Assets** section and open the **Asset Types** tab.
2. Click **Create Asset Type**.
3. Enter a **name** (e.g., ``Industrial Pump``, ``Conveyor Belt``, ``CNC
   Machine``).
4. Optionally add a **description**.
5. Click **Save**.

You only need to create each type once. All specific models and physical
instances will be organized under their respective type.

Step 2: Create an Asset Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An **Asset Model** is a specific product or configuration within a type. More
importantly, it is where you define the **device hierarchy**, the template that
describes which devices this model of equipment needs and how they are
organized.

1. Still in the **Assets** section, click on the **Asset Types** tab and select
   your newly created type.
2. Click **Add Model**.
3. Give it a **name** (e.g., ``XYZ-500 Series``, ``Mark II Conveyor``) and,
   optionally, a **description**.
4. Assign an attribute set to the model (see Part 5 for details about how
   Attribute Sets are created) and click **Next**.
5. Build the model hierarchy by slecting from a list of previously created
   **assets** or **devices** . This is a bluepring describing what components
   your asset model contains.
6. Save the hierarchy when done.
7. Click **Save** to create the model.

.. tip::
   **Think of the hierarchy as a socket diagram.** It describes the *shape* of
   the device setup an asset needs -- the real devices are plugged in during
   commissioning (Step 4 below).

Step 3: Create an Asset Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you create the actual, physical piece of equipment in the system.

1. Go to the main **Assets** list.
2. Click **Add Assets**.
3. Select the **Asset Model** this piece of equipment is based on.
4. Give it a meaningful **name** (e.g., ``Pump-001-HallB``,
   ``Robot-Line3-Position2``).
5. Fill in any other required fields (location, notes, etc.).
6. Click **Save**.

The asset now exists in phyHUB, but its device slots are empty. The next step
fills them.

Step 4: Commission a Device (Link Device to Asset)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Commissioning is the act of assigning a specific physical device -- identified
by its serial number -- to a slot in an asset’s hierarchy. This is the final
connection between the digital platform and the real world.

1. Open the asset instance you just created from the **Assets** list.
2. Navigate to the **Asset Hierarchy/Commissioning** tab and you will see the
   hierarchy blueprint defined by the model.
3. Click on **Assign** for each hierarchy component to assign a device or asset
   to it.
4. Select the device or asset from the list or search by name/serial number.
5. Confirm the assignment.
6. Repeat for all slots in the hierarchy.

Once commissioned, the asset's overview will show the live status of each
connected device, and you can navigate from the asset directly to the device
details page.

--------------

Part 5: Attribute Sets
----------------------

Attribute sets let you attach custom data fields to your asset models -- things
like installation date, manufacturer details, maintenance schedule, maximum
operating temperature, or any other information your team needs to track.

What Is an Attribute Set?
~~~~~~~~~~~~~~~~~~~~~~~~~

An attribute set is a reusable template of data fields. You create it once and
then attach it to one or more asset models. Every asset of that model will then
have those fields available to fill in.

For example, you might create an attribute set called ``Pump Specifications``
containing fields like ``Max Flow Rate``, ``Operating Pressure``, and
``Installation Date``. Attach it to the ``XYZ-500 Series`` model and every
XYZ-500 pump in your system will have those fields.

Creating an Attribute Set
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Go to **Assets** → **Attribute Fields & Sets**.
2. Click **Create Attribute Set** (the “**+**” icon).
3. Give the set a **name** and an optional **description**.
4. After the set is created, select it from the list and click **Add Attribute**
   to add each data field:

   - **Name** -- the label for the field (e.g., ``Max Flow Rate``)
   - **Type** -- the kind of value this field holds:

   =========== ===============================================
   Type        Use it for
   =========== ===============================================
   **String**  Text (names, descriptions, codes)
   **Integer** Whole numbers (counts, IDs)
   **Float**   Decimal numbers (measurements, temperatures)
   **Boolean** Yes / No values
   **Date**    Calendar dates (installation date, expiry date)
   =========== ===============================================

5. Add as many attributes as needed, then click **Save**.

Attaching an Attribute Set to an Asset Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**New model**

When creating a new model you can assign an existing Attribute Set to it duting
the model creation flow.

**Existing model**

You can edit an existing Asset Model to assign a new Attribute Set or remove an
existing set.

1. Go to **Assets** → **Asset Types**.
2. Find the Asset Type that contains the model you want to edit.
3. Click on the **Models** tab to see all the models created for the selected
   asset type.
4. Click on the asset model you want to edit to go to its details page
5. On the asset model details page click **Manage** and select **Edit**
6. You will see the asset model creation form, this time with all the details
   already filled in.
7. All the available attribute sets are listed in the lower half of the page.
   Check the box next to each set you want to add to your model.
8. Click **Next** to confirm no changes need to be done to the hierarchy.
9. Click **Save**.

--------------

Putting It All Together -- A Typical Setup Workflow
---------------------------------------------------

Here is the recommended order of operations when setting up phyHUB for the first
time, or when onboarding a new type of device and equipment:

+-----------------------+-----------------------+-----------------------+
| Step                  | What to do            | Where                 |
+=======================+=======================+=======================+
| 1                     | Provision devices     | Device terminal       |
|                       | physically (run       |                       |
|                       | terminal commands on  |                       |
|                       | the hardware)         |                       |
+-----------------------+-----------------------+-----------------------+
| 2                     | Create your Asset     | phyHUB → Assets →     |
|                       | Types                 | Asset Types           |
+-----------------------+-----------------------+-----------------------+
| 3                     | Create your Asset     | phyHUB → Assets →     |
|                       | Models with device    | Asset Models          |
|                       | hierarchies           |                       |
+-----------------------+-----------------------+-----------------------+
| 4                     | Create Attribute Sets | phyHUB → Assets →     |
|                       | for your asset models | Attribute Sets        |
|                       | (optional but         |                       |
|                       | recommended)          |                       |
+-----------------------+-----------------------+-----------------------+
| 5                     | Upload your           | Device terminal       |
|                       | application packages  |                       |
|                       | to the store          |                       |
+-----------------------+-----------------------+-----------------------+
| 6                     | Have a Software       | phyHUB → Software     |
|                       | Manager review and    |                       |
|                       | rate the apps         |                       |
+-----------------------+-----------------------+-----------------------+
| 7                     | Create a Deployment   | phyHUB → Deployment   |
|                       | Group for the         | Groups                |
|                       | relevant device model |                       |
+-----------------------+-----------------------+-----------------------+
| 8                     | Add the approved apps | phyHUB → Deployment   |
|                       | to the deployment     | Groups → Apps         |
|                       | group                 |                       |
+-----------------------+-----------------------+-----------------------+
| 9                     | Activate your devices | phyHUB → Devices →    |
|                       | in phyHUB             | Activate Device       |
+-----------------------+-----------------------+-----------------------+
| 10                    | Add the registered    | phyHUB → Deployment   |
|                       | devices to the        | Groups → Devices      |
|                       | deployment group      |                       |
+-----------------------+-----------------------+-----------------------+
| 11                    | Create Asset          | phyHUB → Assets       |
|                       | Instances for each    |                       |
|                       | piece of physical     |                       |
|                       | equipment             |                       |
+-----------------------+-----------------------+-----------------------+
| 12                    | Commission each       | phyHUB → Assets →     |
|                       | device to its asset   | [Asset] → Hierarchy   |
|                       | slot                  |                       |
+-----------------------+-----------------------+-----------------------+
| 13                    | Monitor device        | phyHUB → Devices /    |
|                       | status, installation  | Assets                |
|                       | progress, and asset   |                       |
|                       | health                |                       |
+-----------------------+-----------------------+-----------------------+

.. note::
   **You do not have to complete all of these steps in a single
   session.** Many teams set up the asset hierarchy and deployment
   groups once, then add new devices and commission them as new
   equipment arrives on site.

--------------

Frequently Asked Questions
--------------------------

Can I add an app to a deployment group before it has been reviewed?
   It depends on the status. Apps rated **Experimental**, **Edge**, or
   **Stable** all appear in the deployment group app selector and can be
   assigned to devices. Apps with **Unrated** status (freshly uploaded, not yet
   reviewed) or **Denied** status (rejected by a reviewer) do not appear in the
   selector and cannot be deployed.

What happens if I add a device to a deployment group after the group already has apps assigned?
   phyHUB will automatically begin installing all of the group's apps on the
   newly added device. You do not need to trigger this manually.

Can a device belong to more than one deployment group?
   No. A device can only be in one deployment group at a time. If you need a
   device to run a different set of apps, move it to a different group (or
   update the apps in its current group).

Can the same app be assigned to multiple deployment groups?
   Yes. You can add the same app to as many deployment groups as you need.

What is the difference between "Deployment Status" and "Installation Status" on a device?
   -  **Deployment Status** is what phyHUB *wants* the device to have
      (based on its deployment group).
   -  **Installation Status** is what is *actually installed* on the device
      right now. If the two don't match, it means phyHUB is still in the process
      of pushing an update, or there was a failure during installation (check
      the Logs tab for details).

Do I have to commission a device to an asset?
   No. Commissioning is optional. Devices in deployment groups will receive and
   run their apps regardless of whether they are linked to an asset.
   Commissioning is only needed if you want to track which physical equipment
   each device belongs to.

Can I reassign a device to a different asset slot later?
   Yes. You can de-commission a device from its current slot and re-commission it
   to a different one. This is useful when devices are replaced or physically
   moved.
