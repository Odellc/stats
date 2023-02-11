using System;

using Android.App;
using Android.Content.PM;
using Android.OS;


namespace UpwardFarms.Scantron.Droid
{
    using TechnologySolutions.Rfid.AsciiProtocol.Extensions;
    using TechnologySolutions.Rfid.AsciiProtocol.Platform;
    using TechnologySolutions.Rfid.AsciiProtocol.Transports;

    [Activity(Label = "Scantron", Icon = "@drawable/upwardfarms", Theme = "@style/MainTheme", MainLauncher = true, ConfigurationChanges = ConfigChanges.ScreenSize | ConfigChanges.Orientation)]
    public class MainActivity : global::Xamarin.Forms.Platform.Android.FormsAppCompatActivity
    {
        private IAndroidLifecycle lifecyle;

        protected override void OnCreate(Bundle savedInstanceState)
        {
            TabLayoutResource = Resource.Layout.Tabbar;
            ToolbarResource = Resource.Layout.Toolbar;

            base.OnCreate(savedInstanceState);
            Xamarin.Essentials.Platform.Init(this, savedInstanceState);
            Plugin.InputKit.Platforms.Droid.Config.Init(this, savedInstanceState);
            global::Xamarin.Forms.Forms.Init(this, savedInstanceState);

            App app = new App();
            LoadApplication(app);
        }

        private IAndroidLifecycle TslLifecycle
        {
            get
            {
                if (this.lifecyle == null)
                {
                    AsciiTransportsManager manager = Locator.Default.Locate<IAsciiTransportsManager>() as AsciiTransportsManager;

                    // AndrdoidLifecycleNone provides a no action IAndroidLifecycle instance to call in OnPause, OnResume so we don't keep
                    // attempting to resolve the AsciiTransportManager as the IAndroidLifecycle if it is not being used in this project
                    this.lifecyle = (IAndroidLifecycle)manager ?? new AndroidLifecycleNone();

                    // If the HostBarcodeHandler has been registered with the locator then it will be the Android type that needs IAndroidLifecycle calls
                    // Register the HostBarcodeHandler lifecycle with the AsciiTransportsManager
                    manager.RegisterLifecycle(Locator.Default.Locate<IHostBarcodeHandler>() as HostBarcodeHandler);
                }

                return this.lifecyle;
            }
        }

        protected override void OnDestroy()
        {
            base.OnDestroy();

            (this.Lifecycle as IDisposable).Dispose();
        }

        protected override void OnPause()
        {
            base.OnPause();

            this.TslLifecycle.OnPause();
        }

        protected override void OnResume()
        {
            base.OnResume();
            this.TslLifecycle.OnResume(this);
        }

        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, Android.Content.PM.Permission[] grantResults)
        {
            Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);

            base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
    }
}