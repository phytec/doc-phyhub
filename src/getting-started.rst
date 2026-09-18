Getting Started with phyHUB
===========================

Introduction
------------

phyHUB is the update, device, and security management platform of PHYTEC
Messtechnik GmbH, developed in cooperation with our partner MLPA. It
connects your embedded devices in the field to a central platform from
which you control the complete software lifecycle of your fleet.

**Core capabilities:**

-  **Fleet management and remote updates.** Manage your entire device fleet
   online and roll out application (Snap) and operating system (RAUC) updates
   over the air, from a single device to thousands.
-  **Integrated security monitoring.** View CVEs for each individual device and
   deploy fixes directly from the platform. phyHUB integrates seamlessly into
   your existing vulnerability management process.
-  **Role-based access control.** Predefined and freely configurable user roles
   let you cleanly separate development, testing, and rollout responsibilities
   within your team.
-  **Simple hand-off to end customers.** Give your customers access to the full
   platform, or connect a simplified, customer-facing website through the UI.

How This Documentation Is Organized
-----------------------------------

The phyHUB documentation consists of focused manuals that build on each
other. This page is your starting point: it walks you through the
complete path from an empty account to a fully managed device and tells
you which manual to read at each stage.

#. :doc:`Create your account </user-management>`
#. :doc:`Install the phyHUB client and onboard your development kit
   </provisioning>`
#. :doc:`Explore the user interface </ui>`
#. :doc:`Automate and publish from the terminal </cli>`

Follow the steps in this order. Each manual states its prerequisites and
points you to the next document once you are done.

Step 1: Create Your Account
---------------------------

To start evaluating phyHUB, first create an account on your platform instance.
Registration, email verification, inviting your team, and assigning roles are
covered in the:

:doc:`/user-management`

.. note::
   The person who creates the first account automatically becomes the
   Organization Admin of your test instance. This can be changed later, so you
   do not have to make a final decision at this point.

Step 2: Install the phyHUB Client and Onboard Your Device
---------------------------------------------------------

Getting your hardware onto the platform is straightforward. The evaluation runs
on PHYTEC development kits; we provide ready-made images for three platforms:

-  **phyBOARD-Pollux**
-  **phyBOARD-Nash** *(image coming soon)*
-  **phyBOARD-Tauri-L** *(image coming soon)*

Your kit runs the phyHUB image from its internal eMMC storage. You boot the kit
from the SD card it ships with, write the phyHUB image onto the eMMC from there,
and switch the board over to booting from the eMMC. On its first boot from the
eMMC, the device displays a claiming token on its console; you enter this token
on the online platform and the device completes its registration automatically.
Both parts, installing the client and activating the device, are covered in the:

:doc:`/provisioning`

You will need console access to your kit and a network connection with internet
access for the board. The manual lists the exact prerequisites and network setup
before you start.

.. note::
   This token-based flow is intended for evaluation and demonstration purposes.
   For production, PHYTEC provides professional, automated solutions for
   onboarding devices at scale. Contact us for details.

Step 3: Explore the Web Interface
---------------------------------

With your device online, the :doc:`/ui` introduces all functions of the web
platform. Among other things, you will learn how to:

-  Register devices and monitor their status, installation state, and logs
-  Roll out your first application (Snap) update through a deployment group
-  Review, rate, and release uploaded software before it can be deployed
-  Model your physical equipment as assets and commission devices to them
-  Attach custom attribute sets to record equipment data

Step 4: Automate and Publish with the CLI
-----------------------------------------

The :doc:`/cli` documents ``m2cp``, the phyHUB command-line client. It covers
the platform’s device and software management from the terminal and adds
developer capabilities that are not available in the UI:

-  Upload new software, both applications and complete OS images, which then
   becomes available for deployment on the online platform
-  Register new device models to make your machines known to the platform
-  Generate snapd seeds for building custom OS images
-  Claim devices and follow updates live from the terminal

Document Overview
-----------------


========== ======================== ============================================
Order      Document                 Purpose
========== ======================== ============================================
1          :doc:`/user-management`  Organization setup, invitations, user roles
---------- ------------------------ --------------------------------------------
2          :doc:`/provisioning`     Installing the phyHUB client on a PHYTEC
                                    development kit and onboarding it to the
                                    platform
---------- ------------------------ --------------------------------------------
3          :doc:`/ui`               Devices, software, and assets in the web
---------- ------------------------ --------------------------------------------
4          :doc:`/cli`              The ``m2cp`` command-line client
---------- ------------------------ --------------------------------------------
Reference  Role Reference           Detailed permissions of every user role
========== ======================== ============================================

If you have questions at any point during your evaluation, contact the phyHUB
team at PHYTEC. We are happy to help.
