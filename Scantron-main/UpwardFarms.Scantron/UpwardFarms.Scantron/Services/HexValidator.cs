
namespace UpwardFarms.Scantron.Services
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    // Provides validation of Hex strings
    public class HexValidator
    {
        // Characters that can be used to make up the hex value
        private static readonly string hexCharacters = "0123456789abcdefABCDEF";
        // Tests the value is valid Hex and multiple words
        // <param name="value">the string to evaluate</param>
        // <returns>true if the value represents multiple valid Hex words</returns>
        public static bool IsValidWordAlignedHex(string value)
        {
            // Null/empty are defined as invalid
            if (string.IsNullOrEmpty(value))
            {
                return false;
            }

            int count = 0;

            for (int index = 0; index < value.Length; index++)
            {
                if (hexCharacters.Contains(value[index]))
                {
                    count += 1;
                }
                else if (!char.IsWhiteSpace(value[index]))
                {
                    return false;
                }
            }

            // Must be word aligned. Two bytes per word. Two hex characters per byte.
            return count % 4 == 0;
        }
    }
}
