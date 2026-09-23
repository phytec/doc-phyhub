Device Provisioning
===================

This guide walks you through bringing a PHYTEC development kit onto the phyHUB
platform for the first time. It has two parts: In **Part A** you install the
phyHUB client on the internal e.MMC storage of your kit, and in **Part B** you
activate the device on the platform using its claiming token. The whole process
takes about 20 to 30 minutes.

.. note::
   This token-based flow is intended for evaluation and demonstration purposes.
   For production, PHYTEC provides professional, automated solutions for
   onboarding devices at scale.

.. _provisioning-begin:

Before You Begin
----------------

This manual is **Step 2** of the onboarding path described in
:doc:`/getting-started`. Make sure the following prerequisites are met:

1. **A phyHUB account.** If you do not have one yet, complete the
   :doc:`user-management` first. To activate devices, your account needs one of
   the following roles: **Device Manager**, **Device Admin**, **Software
   Developer**, **Software Manager**, or **Software Admin** (see the **Role
   Reference**).
2. **A supported PHYTEC development kit** including the SD card that ships with
   it. The SD card holds a ready-to-boot PHYTEC demo image that you will use in
   :ref:`provisioning-install-client`.
3. **Console access to your board.** We assume you already know how to reach the
   serial console of your board. If not, please refer to the Quick Start Guide
   included with your kit before continuing. This guide uses **SSH** in
   :ref:`provisioning-install-client` and the **UART console** via the debug USB
   port of the board in :ref:`provisioning-activate-device` (115200 baud, 8N1).
4. **A computer** with a web browser, an SSH client (Linux and macOS:
   any terminal; Windows: ``cmd.exe`` or WSL) and a serial terminal
   program (for example PuTTY on Windows, or ``tio``/``screen``/``minicom``
   on Linux and macOS).
5. **Internet access for the board**, needed from
   :ref:`provisioning-activate-device` on. The network setup for both parts is
   described in the next section.

.. note::
   A note on naming The device console output refers to the
   **L-IoT Appstore**. L-IoT is the technology platform that phyHUB is
   built on ("phyHUB, powered by L-IoT"). Wherever the console mentions
   the L-IoT Appstore, enter the token in phyHUB as described in this
   guide.

.. note::
   How to read the commands in this guide Commands prefixed with
   ``host:~$`` are run on your computer. Commands prefixed with
   ``target:~$`` are run on the console of the board. Copy only the part
   after the prefix.

.. _provisioning-network-setup:

Network Setup
~~~~~~~~~~~~~

The two parts of this guide have different network requirements.

**Part A: a link between your computer and the board.** While the kit runs the
PHYTEC demo image from the SD card, it only needs to be reachable from your
computer; internet access is not required. The demo image uses the static IP
address ``192.168.3.11`` on the first Ethernet port. Connect the board to your
computer with a LAN cable (directly or through the same switch) and give your
computer an address in the same subnet, for example ``192.168.3.10`` with
netmask ``255.255.255.0``. If you cannot change your computer’s network
settings, use the UART and USB stick alternative described in Part A instead.

**Part B: internet access and a console.** Once the board runs the phyHUB image
from the e.MMC, you need two connections at the same time: a LAN cable to a
network with internet access, so that the phyHUB client can reach the platform,
and a console to read the claiming token and, if necessary, adjust the network
settings. For the console we recommend the **UART connection** via the debug USB
port, because the IP address the board receives in your network is not known in
advance. SSH works as well once you know that address.

----

.. _provisioning-install-client:

Part A: Install the phyHUB Client on Your Development Kit
---------------------------------------------------------

We have prepared ready-made phyHUB images for three platforms. Each image
contains the complete operating system including the phyHUB client.

.. list-table::
   :header-rows: 1

   *  -  Platform
      -  Image download
      -  PHYTEC BSP manual
   *  -  phyBOARD-Pollux i.MX 8M Plus
      -  https://download.phytec.de/Software/Linux/BSP-Yocto-phyHUB/BSP-Yocto-phyHUB-i.MX8MP-v1.0/
      -  https://phytec.github.io/doc-bsp-yocto/bsp/imx8/imx8mp
   *  -  phyBOARD-Nash i.MX 93
      -  https://download.phytec.de/Software/Linux/BSP-Yocto-phyHUB/BSP-Yocto-phyHUB-i.MX93-v1.0/
      -  https://phytec.github.io/doc-bsp-yocto/bsp/imx9/imx91-93
   *  -  phyGATE-Tauri-L i.MX 8M Mini
      -  https://download.phytec.de/Software/Linux/BSP-Yocto-phyHUB/BSP-Yocto-phyHUB-i.MX8MP-v1.0/
      -  https://www.phytec.de/cdocuments/?doc=doD0F

Your kit is designed to run from its internal **e.MMC** storage, so this is
where the phyHUB image needs to end up. Out of the box, the e.MMC only contains a
bootloader, while the SD card that ships with the kit holds a ready-to-boot
PHYTEC demo image. You will use exactly this SD card system as a helper: boot
the kit from the SD card as described in its Quick Start Guide, stream the
phyHUB image from your computer onto the e.MMC, and finally switch the board
over to booting from the e.MMC.

Throughout Part A you will use the **boot switch** of your board to select
between SD card and e.MMC, and you will need the device name of the e.MMC:

.. list-table::
   :header-rows: 1

   *  -  Platform
      -  Boot switch
      -  SD card position
      -  e.MMC position
      -  e.MMC device
   *  -  phyBOARD-Pollux i.MX 8M Plus
      -  S3 (4-pole DIP switch)
      -  1 = ON, 2--4 = OFF
      -  all OFF
      -  ``/dev/mmcblk2``
   *  -  phyBOARD-Nash
      -  S3 (4-pole DIP switch)
      -  1--2 = ON, 3--4 = OFF
      -  2 = ON, others OFF
      -  ``/dev/mmcblk0``
   *  -  phyGATE-Tauri-L i.MX 8M Mini
      -  1-pole DIP switch (red, reachable through the venting slots of the
         housing
      -  ON
      -  1
      -  ``/dev/mmcblk2``

.. tip::
   The switch positions are also pictured in the Quick Start Guide of your kit.
   You can additionally verify the e.MMC device name on the running board: the
   e.MMC is the MMC device that has ``boot0`` and ``boot1`` entries next to it
   (see Step 3).

Step 1: Download the Image for Your Board
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the ``.partup`` image that matches your development kit from the table
above and save it on your computer.

Step 2: Boot the Kit from Its SD Card
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Set the boot switch of your board to the **SD card** position (see
   the table above).

#. Insert the SD card that ships with your kit.

#. Connect the board to your computer with a LAN cable and make sure
   your computer has an address in the ``192.168.3.x`` subnet (see
   [[#Network Setup]]).

#. Power on the board and wait about a minute for it to boot.

#. Connect to the board via SSH:

   .. code-block:: console

      host:~$ ssh root@192.168.3.11

The board now runs the PHYTEC demo image from the SD card. You do not need to
interact with it otherwise; it is only used to write the e.MMC in the next step.

Step 3: Write the Image to the e.MMC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. In your SSH session, confirm the device name of the e.MMC. The e.MMC is the
   MMC device that has ``boot0`` and ``boot1`` entries. On the phyBOARD-Pollux,
   for example:

   .. code-block:: console

      target:~$ ls /dev | grep mmcblk
      mmcblk1
      mmcblk1p1
      mmcblk1p2
      mmcblk2
      mmcblk2boot0
      mmcblk2boot1
      mmcblk2rpmb

   Here ``mmcblk2`` is the e.MMC and ``mmcblk1`` is the SD card you are
   currently booted from. Leave the SSH session with ``exit``.

2. From your computer, stream the image over SSH directly onto the e.MMC.
   Replace ``<image-file>`` with the decompressed image from Step 1 and the
   device name with the one you confirmed above. The example uses the
   phyBOARD-Pollux:

   .. code-block::

      host:~$ ssh root@192.168.3.11 "dd of=/dev/mmcblk2 bs=1M conv=fsync" < <image-file>

   On Windows, run this command in ``cmd.exe`` or WSL; PowerShell does not
   support the ``<`` redirection. Writing takes a few minutes and produces no
   output until it is finished. Wait until the command returns to the prompt.

.. warning::
   ``dd`` overwrites the target device without asking. Make sure ``of=`` points
   to the e.MMC and not to your SD card.

.. tip::
   Alternative: UART console and USB stick If you cannot or do not want to use
   the network in Part A, you can write the image from a USB stick instead:

   1. Copy the decompressed image to a USB stick formatted with FAT32. Note that
      FAT32 cannot store files larger than 4 GB.

   2. Instead of SSH, open the UART console of the board in your serial terminal
      program (see [[#Before You Begin]]) and log in as ``root``.

   3. Plug the USB stick into the board and write the image from there:

      .. code-block:: console

         target:~$ mount /dev/sda1 /mnt
         target:~$ dd if=/mnt/<image-file> of=/dev/mmcblk2 bs=1M conv=fsync status=progress

   If ``mount`` fails, check which device the stick received with ``ls
   /dev/sd*`` and adjust the command. Remove the stick together with the SD card
   in Step 4.

Step 4: Switch to the e.MMC and Boot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Shut the board down and disconnect the power:

   .. code-block::

      host:~$ ssh root@192.168.3.11 poweroff

2. **Remove the SD card**, so that the board can only boot from the e.MMC. Keep
   it in a safe place; you can use it again at any time to repeat Part A.

3. Set the boot switch to the **e.MMC** position (see the table above).

4. Connect your computer to the debug USB port of the board and open the UART
   console in your serial terminal program. This is where you will read the
   claiming token in Part B.

5. Connect the board to a network with internet access using the LAN cable (see
   [[#Network Setup]]). If your computer was connected directly to the board so
   far, plug the board into your network now; the console connection over USB is
   not affected by this.

6. Reconnect the power. The board now boots the phyHUB image from the e.MMC and
   runs a one-time setup process automatically. This may take a minute or two.
   You can follow the boot output on the serial console.

Once the setup completes, the phyHUB client is installed. Continue with Part B.

--------------

.. _provisioning-activate-device:

Part B: Activate the Device on the Platform
-------------------------------------------

Step 1: Find Your Claiming Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the device has finished its initial setup, a **claiming token** appears on
the serial console. It looks like this::

   [   24.786848] liot-provisioning[709]: +--------------------------------------+
   [   24.789900] liot-provisioning[709]: |    Enter this token in the L-IoT     |
   [   24.791107] liot-provisioning[709]: |     Appstore to bind this device     |
   [   24.792463] liot-provisioning[709]: |           to your account:           |
   [   24.794724] liot-provisioning[709]: |                                      |
   [   24.795887] liot-provisioning[709]: |            PZPS-276Z-3A4E            |
   [   24.798715] liot-provisioning[709]: |                                      |
   [   24.800802] liot-provisioning[709]: +--------------------------------------+

**Write down or copy your token.** You will need to enter it in phyHUB in the
next steps.

.. tip::
   If the token has scrolled off your console, or if you are connected via SSH
   and therefore do not see the boot output, you can display it at any time on
   the console of the board:

   .. code-block:: console

      target:~$ cat /var/lib/snapd/claiming-token

.. note::

   If you power-cycle your device before completing activation, the same token
   will be shown again when it boots. You do not need to start over.

Step 2: Log In to phyHUB
~~~~~~~~~~~~~~~~~~~~~~~~

Open phyHUB in your web browser and sign in with your account.

.. note::
   If you cannot see the **Devices** section after logging in, your account is
   missing one of the roles listed under :ref:`provisioning-begin`. Ask your
   Organization Admin to assign it.

.. _provisioning-enter-claiming-token:

Step 3: Enter Your Claiming Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In phyHUB, navigate to the **Devices** section, click **Activate Device**, enter
the token from Step 1, and click **Save**.

Once you submit the token, phyHUB will link your device to your account. This
activation step is the same one described in Part 1 of the :doc:`/ui`.

.. tip::
   Alternative You can also claim the token from the terminal with ``m2cp device
   claim <token>``. See Part 1 of the :doc:`/cli`.

The device must finish registering within the next **3 hours**. If you run out
of time, see :ref:`provisioning-troubleshooting` below.

Step 4: Wait for Your Device to Register
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your device checks in with the platform automatically in the background
(approximately once per minute). Once it detects that you have entered the
token, it will complete registration on its own.

You do not need to do anything during this step. Just keep the device powered on
and connected to the internet.

Step 5: Confirm Activation
~~~~~~~~~~~~~~~~~~~~~~~~~~

When registration is complete, a confirmation message appears on the
serial console::

   ==========================================

     Device registered successfully.

     OS Serial: 550e8400-e29b-41d4-a716-446655440000

   ==========================================

If you are connected via SSH instead, check the **Devices** list in phyHUB: your
device appears there as soon as registration is complete.

Your **OS Serial** is the unique identifier for your device in phyHUB. Make a
note of it for your records.

Your device is now fully activated and ready to use.

Next Steps
----------

Your device now appears in the **Devices** list of the platform. Continue with
**Step 3** of :doc:`/getting-started`:

- The :doc:`/ui` shows you how to add the device to a deployment group, install
  software on it, and link it to your physical equipment.
- If you prefer working from the terminal, the :doc:`/cli` covers the same
  onboarding flow with the ``m2cp`` client.

.. _provisioning-troubleshooting:

Troubleshooting
---------------

The token expired before registration completed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The 3-hour window starts the moment you enter the token in phyHUB. If
registration did not complete in time, the device will automatically generate a
new token and display it on the serial console. Simply go back to
:ref:`provisioning-enter-claiming-token` and enter the new token.

The device does not show a token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Display the token directly on the console:

   .. code-block:: console

      target:~$ cat /var/lib/snapd/claiming-token

-  Make sure the device has fully finished booting and completed its one-time
   setup.
-  Make sure the board has an active internet connection (see
   :ref:`provisioning-network-setup`).
-  Try power-cycling the device.

You cannot reach the board via SSH in Part A
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Check that your computer has an address in the ``192.168.3.x`` subnet
   and that the LAN cable is connected to the first Ethernet port of the
   board (see :ref:`provisioning-network-setup`).
-  Alternatively, use the UART console and USB stick as described in Part
   A, Step 3.

The board still shows the PHYTEC demo system or does not boot after switching to the e.MMC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Check that the boot switch is in the **e.MMC** position for your board (see
   the table in :ref:`provisioning-install-client`) and that the SD card is
   removed.
-  Make sure the ``dd`` command in Part A, Step 3 completed without an error
   message. If you are unsure, boot from the SD card again and repeat Step 3.

phyHUB says the token is invalid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Check that you typed the token exactly as shown, including any hyphens.
-  The token may have already been used or may have expired. An expired token is
   replaced by a new one automatically (see the first entry above); use the new
   token.
