using System;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using UpwardFarms.Scantron.Views;

[assembly: XamlCompilation(XamlCompilationOptions.Compile)]
namespace UpwardFarms.Scantron
{
    using System.Linq;

    public partial class App : Application
    {         
        public App()
        {
            InitializeComponent();

            MainPage = new MainPage();
        }
        // Gets the <see cref="ViewModels.ViewModelLocator"/> that will return a ViewModel for a View
        public static ViewModels.ViewModelLocator ViewModel { get; } = new ViewModels.ViewModelLocator();

        protected override void OnStart()
        {
            // Handle when your app starts
        }

        protected override void OnSleep()
        {
            // Handle when your app sleeps
        }

        protected override void OnResume()
        {
            // Handle when your app resumes
        }
    }
}
