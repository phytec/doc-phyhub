Getting Started with phyHUB
===========================

Introduction
------------

phyHUB is the update, device, and security management platform of PHYTEC
Messtechnik GmbH, developed in cooperation with our partner MLPA. It
connects your embedded devices in the field to a central platform from
which you control the complete software lifecycle of your fleet.

**Core capabilities:**

- **Fleet management and remote updates.** Manage your entire device
  fleet online and roll out application (Snap) and operating system
  (RAUC) updates over the air, from a single device to thousands.
- **Integrated security monitoring.** View CVEs for each individual
  device and deploy fixes directly from the platform. phyHUB integrates
  seamlessly into your existing vulnerability management process.
- **Role-based access control.** Predefined and freely configurable user
  roles let you cleanly separate development, testing, and rollout
  responsibilities within your team.
- **Simple hand-off to end customers.** Give your customers access to
  the full platform, or connect a simplified, customer-facing website
  through the UI.

--------------

How This Documentation Is Organized
-----------------------------------

The phyHUB documentation consists of focused manuals that build on each
other. This page is your starting point: it walks you through the
complete path from an empty account to a fully managed device and tells
you which manual to read at each stage.

::

   Step 1   Create your account
                └─  User Management Manual

   Step 2   Install the phyHUB client on your hardware
                ├─  Option A: PHYTEC development kit  →  Prebuilt Image Guide (in preparation)
                └─  Option B: Your own hardware       →  Yocto Integration Guide (in preparation)

   Step 3   Onboard your device to the platform
                └─  Device Provisioning Manual

   Step 4   Explore the web interface
                └─  UI Manual

   Step 5   Automate and publish from the terminal
                └─  CLI Manual

Follow the steps in this order. Each manual states its prerequisites and
points you to the next document once you are done.

--------------

Step 1: Create Your Account
---------------------------

To start evaluating phyHUB, first create an account on your platform
instance. Registration, email verification, inviting your team, and
assigning roles are covered in the:

`User Management Manual <01_User_Management_Manual.md>`__

   **Note:** The person who creates the first account automatically
   becomes the Organization Admin of your test instance. This can be
   changed later, so you do not have to make a final decision at this
   point.

--------------

Step 2: Get the phyHUB Client onto Your Device
----------------------------------------------

Onboarding your hardware is straightforward. You install an image
containing the phyHUB client on your device. On first boot, the device
displays a claiming token that you enter on the online platform to bind
the device to your account (Step 3).

Two paths are available, depending on your hardware:

+-----------------------+-----------------------+-----------------------+
| Your hardware         | What to do            | Guide                 |
+=======================+=======================+=======================+
| **PHYTEC development  | Download a ready-made | Prebuilt Image Guide  |
| kit**                 | image and flash it    | *(in preparation)*    |
|                       | onto the kit          |                       |
+-----------------------+-----------------------+-----------------------+
| **Your own hardware** | Build a Yocto image   | Yocto Integration     |
|                       | that includes the     | Guide *(in            |
|                       | phyHUB layer          | preparation)*         |
+-----------------------+-----------------------+-----------------------+

..

   **Note:** This token-based flow is intended for evaluation and
   demonstration purposes. For production, PHYTEC provides professional,
   automated solutions for onboarding devices at scale. Contact us for
   details.

--------------

Step 3: Onboard Your Device to the Platform
-------------------------------------------

Once the phyHUB client is running on your device, you can bring the
device online. The device displays a claiming token on its serial
console; you enter this token on the platform and the device completes
its registration automatically. The full procedure is described in the:

`Device Provisioning Manual <02_Device_Provisioning_Manual.md>`__

   **Note:** The provisioning manual is currently written for PHYTEC
   development kits. Once the phyHUB client is installed, the token flow
   for your own hardware is identical.

--------------

Step 4: Explore the Web Interface
---------------------------------

With your device online, the `UI Manual <03_phyHUB_UI_Manual.md>`__
introduces all functions of the web platform. Among other things, you
will learn how to:

- Register devices and monitor their status, installation state, and
  logs
- Roll out your first application (Snap) update through a deployment
  group
- Review, rate, and release uploaded software before it can be deployed
- Model your physical equipment as assets and commission devices to them
- Attach custom attribute sets to record equipment data

.. raw:: html

   <!-- TODO (author): The original concept also lists "perform a first Snap and RAUC update" and
   "view CVEs" as UI Manual topics. The current UI Manual covers app (Snap) rollout via deployment
   groups, but has no sections on OS (RAUC) updates or CVE views yet. Either extend the UI Manual
   with those sections or keep this list as is. -->

--------------

Step 5: Automate and Publish with the CLI
-----------------------------------------

The `CLI Manual <04_phyHUB_CLI_Manual.md>`__ documents ``m2cp``, the
phyHUB command-line client. It covers the platform’s device and software
management from the terminal and adds developer capabilities that are
not available in the UI:

- Upload new software, both applications and complete OS images, which
  then becomes available for deployment on the online platform
- Register new device models to make your machines known to the platform
- Generate snapd seeds for building custom OS images
- Claim devices and follow updates live from the terminal
