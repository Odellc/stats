using System;

namespace UpwardFarms.Scantron.Models
{
    public class AppConfiguration
        : ViewModels.ViewModelBase
    {
        private bool enableManualId;
        private bool enableTestId;
        private double powerLevel;
        private double powerLevelInfo;
        private double powerLevelJob;
        private double powerLevelInventory;
        private string host;
        private string customHost;
        private string companyId;
        private string companyName;

        // Default Hosts
        private const string MAIN_HOST = "https://api.businesscentral.dynamics.com/v2.0/b24c33e0-6bbf-4163-82d2-7d897a653311/Production/";
        private const string MAIN_COMPANY_ID = "cbb6d286-353b-eb11-846f-002248203226";
        private const string MAIN_COMPANY_NAME = "Upward%20Farms";
        private const string TEST_HOST = "https://api.businesscentral.dynamics.com/v2.0/b24c33e0-6bbf-4163-82d2-7d897a653311/sandboxInflux/";
        private const string TEST_COMPANY_ID = "8a8c523b-69e0-eb11-86df-00224822b645";
        private const string TEST_COMPANY_NAME = "Upward%20Farms";
        private const string CUST_HOST = "https://api.myhost.com/";

        // Other pieces needed for generating URI's
        private const string POST_PREFIX = "ODataV4";
        private const string GET_PREFIX = "api/INECTA/RFIDScanner/v2.0";
        private const string AUTH_CODE = "RFlOQU1JQ1M6QWIxVFYxaVJQZFM0Q1grUjNyOG9mSW9PUnV5V2VSU3lpc25GRDEzY2VyMD0=";

        public AppConfiguration()
        {
            // Load or Default Manual Toggle
            if (App.Current.Properties.ContainsKey("enable_manual_id"))
            {
                enableManualId = Convert.ToBoolean(App.Current.Properties["enable_manual_id"] as string);
            }
            else
            {
                enableManualId = false;
            }

            // Load or Default Test Toggle 
            if (App.Current.Properties.ContainsKey("enable_test_id"))
            {
                enableTestId = Convert.ToBoolean(App.Current.Properties["enable_test_id"] as string);
            }
            else
            {
                enableTestId = false;
            }

            // Load or Default Power Level Info
            if (App.Current.Properties.ContainsKey("power_level_info"))
            {
                powerLevelInfo = Convert.ToDouble(App.Current.Properties["power_level_info"] as string);
            }
            else
            {
                powerLevelInfo = 40.0;
            }
            powerLevel = powerLevelInfo;

            // Load or Default Power Level Job
            if (App.Current.Properties.ContainsKey("power_level_job"))
            {
                powerLevelJob = Convert.ToDouble(App.Current.Properties["power_level_job"] as string);
            }
            else
            {
                powerLevelJob = 50.0;
            }

            // Load or Default Power Level Inventory
            if (App.Current.Properties.ContainsKey("power_level_inventory"))
            {
                powerLevelInventory = Convert.ToDouble(App.Current.Properties["power_level_inventory"] as string);
            }
            else
            {
                powerLevelInventory = 20.0;
            }

            // Load or Default Custom Host
            if (App.Current.Properties.ContainsKey("custom_host"))
            {
                customHost = App.Current.Properties["custom_host"] as string;
            }
            else
            {
                customHost = CUST_HOST;
            }

            // Load or Default Current Host
            if (App.Current.Properties.ContainsKey("current_host"))
            {
                host = App.Current.Properties["current_host"] as string;
            }
            else
            {
                host = TEST_HOST;
            }

            // Load or Default Company Id
            if (App.Current.Properties.ContainsKey("company_id"))
            {
                companyId = App.Current.Properties["company_id"] as string;
            }
            else
            {
                companyId = TEST_COMPANY_ID;
            }

            // Load or Default Company Name
            if (App.Current.Properties.ContainsKey("company_name"))
            {
                companyName = App.Current.Properties["company_name"] as string;
            }
            else
            {
                companyName = TEST_COMPANY_NAME;
            }
        }

        public bool EnableManualId
        {
            get
            {
                return enableManualId;
            }

            set
            {
                App.Current.Properties["enable_manual_id"] = value.ToString();
                App.Current.SavePropertiesAsync();
                this.Set(ref enableManualId, value);
            }
        }

        public bool EnableTestId
        {
            get
            {
                return enableTestId;
            }

            set
            {
                App.Current.Properties["enable_test_id"] = value.ToString();
                App.Current.SavePropertiesAsync();
                this.Set(ref enableTestId, value);
            }
        }

        public double PowerLevelInfo
        {
            get
            {
                return powerLevelInfo;
            }

            set
            {
                App.Current.Properties["power_level_info"] = value.ToString();
                App.Current.SavePropertiesAsync();
                this.Set(ref powerLevelInfo, value);
            }
        }

        public double PowerLevelJob
        {
            get
            {
                return powerLevelJob;
            }

            set
            {
                App.Current.Properties["power_level_job"] = value.ToString();
                App.Current.SavePropertiesAsync();
                this.Set(ref powerLevelJob, value);
            }
        }

        public double PowerLevelInventory
        {
            get
            {
                return powerLevelInventory;
            }

            set
            {
                App.Current.Properties["power_level_inventory"] = value.ToString();
                App.Current.SavePropertiesAsync();
                this.Set(ref powerLevelInventory, value);
            }
        }

        public string Host
        {
            get
            {
                return host;
            }

            set
            {
                // Update Host
                App.Current.Properties["current_host"] = value;
                App.Current.SavePropertiesAsync();
                this.Set(ref host, value);

                // If it's a built-in host, also update Company Info
                if (value == MAIN_HOST)
                {
                    CompanyId = MAIN_COMPANY_ID;
                    CompanyName = MAIN_COMPANY_NAME;
                }
                else if (value == TEST_HOST)
                {
                    CompanyId = TEST_COMPANY_ID;
                    CompanyName = TEST_COMPANY_NAME;
                }
            }
        }

        public string HostCustom
        {
            get
            {
                return customHost;
            }

            set
            {
                App.Current.Properties["custom_host"] = value;
                App.Current.SavePropertiesAsync();
                this.Set(ref customHost, value);
            }
        }

        public string HostMain
        {
            get => MAIN_HOST;
        }

        public string HostTest
        {
            get => TEST_HOST;
        }

        public string AuthCode
        {
            get => AUTH_CODE;
        }

        public string CompanyId
        {
            get => companyId;

            set
            {
                App.Current.Properties["company_id"] = value;
                App.Current.SavePropertiesAsync();
                this.Set(ref companyId, value);
            }
        }

        public string CompanyName
        {
            get => companyName;

            set
            {
                App.Current.Properties["company_name"] = value;
                App.Current.SavePropertiesAsync();
                this.Set(ref companyName, value);
            }
        }

        public string GenerateGetUri(string suffix)
        {
            return host + GET_PREFIX + "/companies(" + companyId + ")" + suffix;
        }

        public string GeneratePostUri(string suffix)
        {
            return host + POST_PREFIX + suffix + "?Company=" + companyName;
        }

        public string GenerateGetBaseUri(string suffix)
        {
            return host + GET_PREFIX + suffix;
        }
    }
}
