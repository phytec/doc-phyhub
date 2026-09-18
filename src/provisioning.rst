Activating Your phyHUB Devkit Device
====================================

This guide walks you through activating your L-IoT dev kit for the first
time. The process takes about 5–10 minutes.

--------------

What you will need
------------------

- Your devkit device

- A computer with access to the **phyHUB Appstore** (a web browser is
  enough)

- A serial console connection to your device (e.g. a USB-to-serial cable
  and a terminal application such as PuTTY or screen)

- Your Appstore login credentials.

--------------

Step 1 — Power on your device
-----------------------------

Connect power to your device and let it boot up for the first time. Make
sure it has an active internet connection.

   Your device will begin a one-time setup process automatically. This
   may take a minute or two.

--------------

Step 2 — Find your claiming token
---------------------------------

Once the device has finished its initial setup, a **claiming token**
will appear on the serial console. It looks like this:

::


   [   24.786848] liot-provisioning[709]: +--------------------------------------+
   [   24.789900] liot-provisioning[709]: |    Enter this token in the L-IoT     |
   [   24.791107] liot-provisioning[709]: |     Appstore to bind this device     |
   [   24.792463] liot-provisioning[709]: |           to your account:           |
   [   24.794724] liot-provisioning[709]: |                                      |
   [   24.795887] liot-provisioning[709]: |            PZPS-276Z-3A4E            |
   [   24.798715] liot-provisioning[709]: |                                      |
   [   24.800802] liot-provisioning[709]: +--------------------------------------+

**Write down or copy your token.** You will need to enter it in the
Appstore in the next step.

   **Note:** If you power-cycle your device before completing
   activation, the same token will be shown again when it boots, you do
   not need to start over.

..

   If you need to use a new token, you can press Alt+R in the serial
   line. This will trigger a device reboot and a new token will be
   generated.

--------------

Step 3 — Log in to the phyHUB Appstore
--------------------------------------

Open the **phyHUB Appstore** in your web browser and sign in with your
account.

   | **Note:**: you need to have one of the following user roles: -
     Device Manager
   | - Device Admin
   | - Software Developer
   | - Software Manager
   | - Software Admin

--------------

Step 4 — Enter your claiming token
----------------------------------

In the phyHUB web UI, navigate to the device activation or claiming
section and enter the token from Step 2.

Once you submit the token, the Appstore will link your device to your
account.

The device must finish registering within the next 3 hours. If you run
out of time, see `If something goes wrong <#if-something-goes-wrong>`__
below.

--------------

Step 5 — Wait for your device to register
-----------------------------------------

Your device checks in with the Appstore automatically in the background
(approximately once per minute). Once it detects that you have entered
the token, it will complete registration on its own.

You do not need to do anything during this step, just keep the device
powered on and connected to the internet.

--------------

Step 6 — Confirm activation
---------------------------

When registration is complete, a confirmation message will appear on the
serial console:

::


   ============================================

     Device registered successfully.



     OS Serial: 550e8400-e29b-41d4-a716-446655440000

   ============================================

Your **OS Serial** is the unique identifier for your device in the
Appstore. Make a note of it for your records.

Your device is now fully activated and ready to use.

--------------

If something goes wrong
-----------------------

The token expired before registration completed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The 3-hour window starts the moment you enter the token in the Appstore.
If registration did not complete in time, the device will automatically
generate a new token and display it on the serial console. Simply go
back to **Step 3** and enter the new token.

You want a fresh token at any time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to restart the process for any reason, you can request a new
token directly from the device console by pressing Alt+R in the serial
line. Follow the on-screen prompt to confirm, and a new token will be
generated and displayed.

The device does not show a token on boot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Check that your serial console connection is set up correctly.

- Make sure the device has fully finished booting before expecting the
  token to appear.

- Try power-cycling the device.

The Appstore says the token is invalid
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Check that you typed the token exactly as shown, including any
  hyphens.

- The token may have already been used or may have expired. Request a
  new token from the device (see above).
