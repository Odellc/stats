
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

    // View model for the inventory of companies
    public class CompanyInventory
    {
        // parameters and commands for Business Central API
        private const string COMMAND = "/companies";

        // Collection of Currently Active Companies
        public ObservableCollection<FarmCompanyInfo> Companies { get; private set; }

        // Client for Requesting API data 
        private System.Net.Http.HttpClient client;

        private AppConfiguration appConfiguration;

        // Init new instance of Inventory structure
        public CompanyInventory(AppConfiguration appConfiguration)
        {
            this.appConfiguration = appConfiguration;
            this.Companies = new ObservableCollection<FarmCompanyInfo>();

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
            this.Companies.Clear();
        }

        // HttpGet From API 
        public class HttpGet
        {
            public int Id { get; set; }
            public string Title { get; set; }
            public string Body { get; set; }
        }

        public async Task Refresh() 
        {
            try
            {
                Companies.Clear();

                // Build up a request and send it to fetch company list from this server
                var request = appConfiguration.GenerateGetBaseUri(COMMAND);
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

                        // Find each company in the collection (if there are any)
                        regex = new Regex("(\\{[^\\{\\}]*\\})");
                        foreach (Match itemMatch in regex.Matches(collection))
                        {
                            var model = JsonConvert.DeserializeObject<FarmCompanyInfo>(itemMatch.Groups[1].Value);
                            model.valid = true;
                            if (Companies.IndexOf(model) < 0)
                            {
                                Companies.Add(model);
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
