
namespace UpwardFarms.Scantron.Models
{
    using System;
    using System.Collections.Generic;
    using System.Collections.ObjectModel;
    using System.Net.Http.Headers;
    using System.Text;
    using System.Text.RegularExpressions;
    using System.Threading.Tasks;
    using Newtonsoft.Json;

    // View model for the inventory of scan jobs
    public class ScanJobInventory
    {
        // parameters and commands for Business Central API
        private const string PARAMS_URL = "?$filter=scannerId eq '{0}'";
        private const string COMMAND = "/overSeedRPO";

        // Collection of Currently Active Rescan Jobs
        public ObservableCollection<FarmRescanJobInfo> Jobs { get; private set; }

        // Client for Requesting API data 
        private System.Net.Http.HttpClient client;

        private AppConfiguration appConfiguration;

        // Init new instance of Inventory structure
        public ScanJobInventory(AppConfiguration appConfiguration)
        {
            this.appConfiguration = appConfiguration;
            this.Jobs = new ObservableCollection<FarmRescanJobInfo>();

            // Create an HTTP interface
            this.client = new System.Net.Http.HttpClient();
            client.BaseAddress = new Uri(appConfiguration.GenerateGetUri(COMMAND));
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("*/*"));
            client.DefaultRequestHeaders.TryAddWithoutValidation("Accept-Encoding", "gzip, deflate, br");
            client.DefaultRequestHeaders.TryAddWithoutValidation("Connection", "keep-alive");
            client.DefaultRequestHeaders.TryAddWithoutValidation("Cache-Control", "no-chache");

            System.Net.Http.Headers.AuthenticationHeaderValue ahv = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", appConfiguration.AuthCode);
            client.DefaultRequestHeaders.Authorization = ahv;
        }


        // Reset all of the statistics
        public void Clear()
        {
            this.Jobs.Clear();
        }

        // HttpGet From API 
        public class HttpGet
        {
            public int Id { get; set; }
            public string Title { get; set; }
            public string Body { get; set; }
        }

        public async Task Refresh(string scannerId) 
        {
            try
            {
                Jobs.Clear();

                // Build up a request and send it to fetch data about this Raft
                var request = appConfiguration.GenerateGetUri(COMMAND) + String.Format(PARAMS_URL, scannerId);
                var response = await client.GetAsync(request);
                if (response.StatusCode == System.Net.HttpStatusCode.OK)
                {
                    var responseString = await response.Content.ReadAsStringAsync();

                    // Find the collection in the response (if it's there)
                    Regex regex = new Regex("\"value\"\\s*:\\s*\\[([^\\[\\]]*)\\]");
                    Match match = regex.Match(responseString);

                    if (match.Success)
                    {
                        var collection = match.Groups[1].Value;

                        // Find each job in the collection (if there are any)
                        regex = new Regex("(\\{[^\\{\\}]*\\})");
                        foreach (Match itemMatch in regex.Matches(collection))
                        {
                            var model = JsonConvert.DeserializeObject<FarmRescanJobInfo>(itemMatch.Groups[1].Value);
                            model.valid = true;
                            if ((Jobs.IndexOf(model) < 0) && (model.noOfRafts > 0))
                            {
                                Jobs.Add(model);
                            }
                        } 
                    }
                }
            }
            catch 
            {
            }
        }
    }
}
