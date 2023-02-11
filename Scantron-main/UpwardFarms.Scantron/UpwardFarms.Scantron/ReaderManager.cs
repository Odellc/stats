using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace TechnologySolutions.Rfid
{
    public interface IReaderManager
    {
        // Raised when an <see cref="IReader"/> is Connecting, Connected, Disconnecting, Disconnected
        event EventHandler<ReaderEventArgs> ReaderChanged;
        // Raised when the <see cref="ActiveReader"/> changes
        // <remarks>
        // This behaves as an ActiveReader changing/changed event.
        // <list type="bullet">
        // <item>Changing - Disconnecting. The current reader is going away, do any configuration then release it</item>
        // <item>Changed - Connected. This is a new reader to use</item>
        // <item>Lost = Disconnected. The reader is no longer available release reference but it is not there to communicate with</item>
        // </list>
        // </remarks>
        event EventHandler<ReaderEventArgs> ActiveReaderChanged;
        // Gets or sets a reference to the Active reader
        IReader ActiveReader { get; set; }        

        ReaderStates ActiveReaderState { get; }
        // Disconnect the specified reader
        // <param name="reader">The reader to disconnect</param>
        // <returns>A task to disconnect the specified reader</returns>
        Task DisconnectReaderAsync(IReader reader);
    }
    // <see cref="EventArgs"/> for a <see cref="IReader"/> change event
    public class ReaderEventArgs
        : EventArgs
    {
        // Initializes a new instance of the ReaderEventArgs class
        // <param name="reader">The reader that changed</param>
        // <param name="state">The new reader state</param>
        public ReaderEventArgs (IReader reader, ReaderStates state)
        {
            this.Reader = reader;
            this.State = state;
        }
        // Gets the connection state of the reader
        public ReaderStates State { get; private set; }
        // Gets the reader
        public IReader Reader { get; private set; }
    }
    // Provides connection state for the IReader
    public enum ReaderStates
    {
        //Available = TechnologySolutions.Rfid.AsciiProtocol.Transports.ConnectionState.Available,
        Connected = TechnologySolutions.Rfid.AsciiProtocol.Transports.ConnectionState.Connected,
        Connecting = TechnologySolutions.Rfid.AsciiProtocol.Transports.ConnectionState.Connecting,
        Disconnected = TechnologySolutions.Rfid.AsciiProtocol.Transports.ConnectionState.Disconnected,
        Disconnecting = TechnologySolutions.Rfid.AsciiProtocol.Transports.ConnectionState.Disconnecting,
        Interrupted = TechnologySolutions.Rfid.AsciiProtocol.Transports.ConnectionState.Interrupted,
        Lost = TechnologySolutions.Rfid.AsciiProtocol.Transports.ConnectionState.Lost,
        //NotAvailable = TechnologySolutions.Rfid.AsciiProtocol.Transports.ConnectionState.NotAvailable
    }   
}
