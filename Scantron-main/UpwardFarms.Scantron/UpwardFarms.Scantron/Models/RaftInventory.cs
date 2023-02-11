
namespace UpwardFarms.Scantron.Models
{
    using System;
    using System.Collections.Generic;
    using System.Collections.ObjectModel;
    using System.Net.Http;
    using System.Net.Http.Headers;
    using System.Text;
    using System.Text.RegularExpressions;
    using System.Threading.Tasks;
    using Microsoft.AspNetCore.WebUtilities;
    using Newtonsoft.Json;
    using Services;
    using TechnologySolutions.Rfid;
    using TechnologySolutions.Rfid.AsciiProtocol;
    // View model for the inventory of transponders and barcodes
    public class RaftInventory
    {
        // parameters and commands for Business Central API
        private const string PARAMS_URL = "?$filter=rFIDToken eq '{0}'";
        private const string COMMAND_REQ_INFO = "/rfidInformation";
        private const string COMMAND_PUT_RFID = "/inboundProdInfluxRfids";
        private const string COMMAND_FINALIZE_JOB = "/influxRfidMgt_validateScannedRfids";
        private const string COMMAND_CLEAR_JOB = "/influxRfidMgt_clearScannedRfids";

        // Reports transponders seen to the model
        private IMonitorRafts monitorTransponders;
        // Used to invoke actions on the user interface thread
        private IProgress<TranspondersEventArgs> dispatcher;
        // Used to normalize the RSSI signal
        private ISignalNormalization signal;

        // Method of calling back with the total count
        public delegate void OnCountUpdatedDelegate(int newCount);
        public OnCountUpdatedDelegate OnCountUpdated;

        private AppConfiguration appConfiguration;

        // Manual and Simulation Support
        private readonly string[] simulatedRafts = { "AAA00005", "AAA00030", "AAA00035", "AAA00060", "AAA00066", "AAA00067", "AAA00068", "AAA00091", "AAA00092", "AAA00149",
                                                     "AAA00006", "AAA00031", "AAA00036", "AAA00061", "AAA00069", "AAA00070", "AAA00071", "AAA00093", "AAA00094", "AAA00150",};
        private int simulatedRaftCounter = 0;

        // Client for Requesting API data 
        private System.Net.Http.HttpClient client;
        // Initializes a new instance of the TransponderInventory class
        // <param name="statistics">The model to update with inventory statistics</param>
        // <param name="monitorTransponders">Reports transponders inventory</param>
        // <param name="signal">Used to normalize RSSI values</param>
        public RaftInventory(InventoryStatistics statistics, IMonitorRafts monitorTransponders, ISignalNormalization signal, AppConfiguration appConfiguration)
        {
            this.monitorTransponders = monitorTransponders;
            this.appConfiguration = appConfiguration;

            this.dispatcher = new Progress<TranspondersEventArgs>(this.AddTransponders);
            this.signal = signal;
            this.Statistics = statistics;
            this.Identifiers = new ObservableCollection<IdentifiedItem>();

            // Create an HTTP interface
            this.client = new System.Net.Http.HttpClient();
            client.BaseAddress = new Uri(appConfiguration.GenerateGetUri(COMMAND_REQ_INFO));
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("*/*"));
            client.DefaultRequestHeaders.TryAddWithoutValidation("Accept-Encoding", "gzip, deflate, br");
            client.DefaultRequestHeaders.TryAddWithoutValidation("Connection", "keep-alive");
            client.DefaultRequestHeaders.TryAddWithoutValidation("Cache-Control", "no-chache");

            System.Net.Http.Headers.AuthenticationHeaderValue ahv = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", appConfiguration.AuthCode);
            client.DefaultRequestHeaders.Authorization = ahv;

            monitorTransponders.TranspondersReceived += (sender, e) =>
            {
                if (this.IsEnabled)
                {
                    this.dispatcher.Report(e);
                }
            };
        }
        // Gets or sets a value indicating whether to append received transponders to the Identifiers collection
        public bool IsEnabled
        {
            get
            {
                return this.monitorTransponders.IsEnabled;
            }

            set
            {
                this.monitorTransponders.IsEnabled = value;
            }
        }
        // Gets the statistics for the transponders scanned
        public InventoryStatistics Statistics { get; private set; }
        // Gets the transponders scanned
        public ObservableCollection<IdentifiedItem> Identifiers { get; private set; }
        // Adds the transponders to the displayed list updating the statistics
        // <param name="transponders">The transponders to add</param>
        // <param name="endPass">True if this update is the last for this inventory pass</param>
        //public void AddTransponders(IEnumerable<TechnologySolutions.Rfid.AsciiProtocol.TransponderData> transponders, bool endPass)
        public async void AddTransponders(TranspondersEventArgs transpondersChunk)
        {
            int unique = 0;
            int seen = 0;
            foreach (var transponder in transpondersChunk.Transponders)
            {
                seen += 1;
                var rssi = transponder.Rssi.HasValue ? this.signal.Normalize(transponder.Rssi.Value) : IdentifiedItem.NoSignal;
                if (await AddTransponderAsync(transponder.Epc, rssi, transponder.Timestamp))
                {
                    unique += 1;
                }
            }

            this.Statistics.Update(unique, seen, transpondersChunk.EndOfPass);
        }

        public async Task<bool> AddTransponderAsync(string epc, double rssi, System.DateTime timestamp)
        {
            bool retval = false;

            // Find EPC in the Identifier List
            IdentifiedItem item = null;
            foreach (var identifier in this.Identifiers)
            {
                if (identifier.Identifier == epc)
                {
                    item = identifier;
                    break;
                }
            }

            // If EPC not already in our Identifier List, Create a New One and Add It
            if (item == null)
            {
                // Add the Idenfified Item to our hash of all unique items.
                item = new IdentifiedItem(epc);

                // Insert the new Identifier Alphabetically to our Displayable List
                bool inserted = false;
                for (int i=0; i < this.Identifiers.Count; i++)
                {
                    if (epc.CompareTo(this.Identifiers[i].Identifier) < 0)
                    {
                        this.Identifiers.Insert(i, item);
                        inserted = true;
                        break;
                    }
                }
                if (!inserted)
                {
                    this.Identifiers.Add(item);
                }

                // Update the Count If There is a Callback For That
                if (this.OnCountUpdated != null)
                {
                    this.OnCountUpdated(this.Identifiers.Count);
                }

                retval = true;
            }

            // Update the viewable item's fields
            item.Seen(timestamp);
            item.NormalizedSignal = rssi;
            var raftInfo = await OnFetchInfo(epc);
            item.Update(raftInfo);

            return retval;
        }

        // Reset all of the statistics
        public void Clear()
        {
            this.Identifiers.Clear();
            this.Statistics.Clear();
            this.signal.Reset();
            if (this.OnCountUpdated != null)
            {
                this.OnCountUpdated(this.Identifiers.Count);
            }
        }

        // HttpGet From API 
        public class HttpGet
        {
            public int Id { get; set; }
            public string Title { get; set; }
            public string Body { get; set; }
        }

        // Create Simulated Raft ID
        private string createSimulatedRaftId(int id)
        {
            return simulatedRafts[id % simulatedRafts.Length];
        }

        public async Task<FarmRaftInfo> OnFetchInfo(string epc) 
        {
            try
            {
                // If we're simulating the Raft ID's replace the EPC with one in the test database
                if (appConfiguration.EnableTestId)
                {
                    epc = createSimulatedRaftId(++simulatedRaftCounter);
                }

                // Build up a request and send it to fetch data about this Raft
                var request = appConfiguration.GenerateGetUri(COMMAND_REQ_INFO) + String.Format(PARAMS_URL, epc);
                var response = await client.GetAsync(request);
                if (response.StatusCode == System.Net.HttpStatusCode.OK)
                {
                    var responseString = await response.Content.ReadAsStringAsync();

                    Regex regex = new Regex("\"value\"\\s*:\\s*\\[([^\\[\\]]*)\\]");
                    Match match = regex.Match(responseString);

                    if (match.Success)
                    {
                        var value = match.Groups[1].Value;
                        var model = JsonConvert.DeserializeObject<FarmRaftInfo>(value);
                        model.valid = true;
                        return model;
                    }

                    return new FarmRaftInfo(false);
                }
                else if (response.StatusCode == System.Net.HttpStatusCode.Unauthorized)
                {
                    //TODO we may need to maybe re-authenticate here
                    return new FarmRaftInfo(false);
                }
                else
                {
                    return new FarmRaftInfo(false);
                }
            }
            catch 
            {
                return new FarmRaftInfo(false);
            }
        }

        // Post Collection of Raft Id's As Complete Job
        public async Task<string> PostRescanJob(string JobProdNum, int NumRaftsDesired)
        {
            if (NumRaftsDesired != Identifiers.Count)
            {
                return "Please Verify Number of Rafts Scanned Before Submitting";
            }

            try
            {
                // Start by Clearing any parts of the job that may have previously been submitted
                var clear_uri = appConfiguration.GeneratePostUri(COMMAND_CLEAR_JOB);
                var clear_content = new StringContent("{ \"prodOrderNo\" : \"" + JobProdNum + "\" }", Encoding.UTF8, "application/json");
                var clear_response = await client.PostAsync(clear_uri, clear_content);
                var clear_resp_content = clear_response.Content;
                if (clear_response.StatusCode != System.Net.HttpStatusCode.OK)
                {
                    var responseString = await clear_response.Content.ReadAsStringAsync();
                    var error = "Failed to Clear Job '" + JobProdNum + "'. ";
                    Regex regex = new Regex("<message>(.*)</message>");
                    Match match = regex.Match(responseString);
                    if (match.Success)
                    {
                        error += match.Groups[1].Value;
                    }
                    return error;
                }

                // Build up a request with each of the raft Id's and post them to the server
                int i = 0;
                var RightNow = DateTime.Now.ToString("yyyy-MM-ddTHH\\:mm\\:ss.fffZ");
                foreach (IdentifiedItem item in Identifiers)
                {
                    // If we're simulating id's, replace as we go.
                    if (appConfiguration.EnableTestId)
                    {
                        item.Identifier = createSimulatedRaftId(i % simulatedRafts.Length);
                    }

                    // Build the body of the message to post the Raft information
                    // (Yes, it's correct that we're generating a GET uri and then POST to it.
                    //  This is an inconsistency in iNECTA's API).
                    i++;
                    var rfid_uri = appConfiguration.GenerateGetUri(COMMAND_PUT_RFID);
                    var rfid_body_hash = new Dictionary<string, string>
                    {
                        ["prodOrderNo"] = JobProdNum,
                        ["entryNo"] = i.ToString(),
                        ["rfidToken"] = item.Identifier,
                        ["scannedDateTime"] = RightNow
                    };

                    // Post RFID to server
                    var rfid_body_text = JsonConvert.SerializeObject(rfid_body_hash);
                    var rfid_content = new StringContent(rfid_body_text, Encoding.UTF8, "application/json");
                    var rfid_response = await client.PostAsync(rfid_uri, rfid_content);
                    if ((rfid_response.StatusCode != System.Net.HttpStatusCode.OK) && (rfid_response.StatusCode != System.Net.HttpStatusCode.Created))
                    {
                        var responseString = await rfid_response.Content.ReadAsStringAsync();
                        var error = "Failed to Post RFID '" + item.RFID + "'. ";
                        Regex regex = new Regex("<message>(.*)</message>");
                        Match match = regex.Match(responseString);
                        if (match.Success)
                        {
                            error += match.Groups[1].Value;
                        }
                        return error;
                    }
                }

                // We've posted all the details. Now we finalize
                var final_uri = appConfiguration.GeneratePostUri(COMMAND_FINALIZE_JOB);
                var final_content = new StringContent("{ \"prodOrderNo\" : \"" + JobProdNum + "\" }", Encoding.UTF8, "application/json");
                var final_response = await client.PostAsync(final_uri, final_content);
                var final_resp_content = final_response.Content;
                if (final_response.StatusCode != System.Net.HttpStatusCode.OK)
                {
                    var responseString = await final_response.Content.ReadAsStringAsync();
                    var error = "Failed to Post Job '" + JobProdNum + "'. ";
                    Regex regex = new Regex("<message>(.*)</message>");
                    Match match = regex.Match(responseString);
                    if (match.Success)
                    {
                        error += match.Groups[1].Value;
                    }
                    return error;
                }
            }
            catch (Exception ex)
            {
                return "Failed to Update. " + ex;
            }

            return "";
        }
    }
}
