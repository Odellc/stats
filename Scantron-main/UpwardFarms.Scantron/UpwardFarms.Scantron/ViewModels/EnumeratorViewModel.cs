
namespace UpwardFarms.Scantron.ViewModels
{
    using System;
    using System.Collections.Generic;
    using System.Runtime.CompilerServices;
    using System.Text;
    using System.Windows.Input;

    using TechnologySolutions.Rfid.AsciiProtocol.Transports;

    using Xamarin.Forms;
    // A visual representation of a <see cref="IAsciiTransportEnumerator"/>
    public class EnumeratorViewModel
        : ViewModelBase
    {
        // The model we're representing
        private IAsciiTransportEnumerator model;
        // Used to update the view based on changes to the model
        private IProgress<IAsciiTransportEnumerator> modelView;
        // Initializes a new instance of the EnumeratorViewModel class
        // <param name="model">The model to represent</param>
        public EnumeratorViewModel(IAsciiTransportEnumerator model)
        {
            this.model = model ?? throw new ArgumentNullException("model");
            this.modelView = new Progress<IAsciiTransportEnumerator>(this.UpdateFromModel);
            this.model.StateChanged += (sender, e) => { this.modelView.Report(this.model); };

            this.State = this.model.State.ToString();
            this.StartEnumeratorCommand = new Command(() => this.ExecuteStartEnumerator());
            this.StopEnumeratorCommand = new Command(() => this.ExecuteStopEnumerator());
        }

        public ICommand StartEnumeratorCommand { get; private set; }

        public ICommand StopEnumeratorCommand { get; private set; }
        // Gets the current state of the enumerator
        public string State
        {
            get => this.state;
            private set => this.Set(ref this.state, value);
        }
        private string state;
        // Gets the transport used by the enumerator
        public string Transport => this.model.Physical.ToString();
        // Updates the ViewModel as the model changes
        // <param name="enumerator">The model that changed</param>
        private void UpdateFromModel (IAsciiTransportEnumerator enumerator)
        {
            this.State = enumerator.State.ToString();
        }

        private void ExecuteStartEnumerator()
        {
            try
            {
                this.model.Start();
            }
            catch (Exception ex)
            {
                ReportError(ex);
            }
        }

        private void ExecuteStopEnumerator()
        {
            try
            {
                this.model.Stop();
            }
            catch (Exception ex)
            {
                ReportError(ex);
            }
        }        
    }
}
