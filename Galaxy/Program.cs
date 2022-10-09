using System.Text;

string rootDir = "";
int GAIA_RA_COL = 1;
int GAIA_DEC_COL = 2;

int GALEX_RA_COL = 4;
int GALEX_DEC_COL = 5;
float APPROX_DETLA = .00001f;

Console.WriteLine("Root dir");
rootDir = Console.ReadLine();

Console.WriteLine("Enver a value for approx delta (default is .00001), press enter to accept default.");
string usersDelta = Console.ReadLine();
if(string.IsNullOrWhiteSpace(usersDelta) == false)
{
    float.TryParse(usersDelta, out APPROX_DETLA);
}

if (System.IO.Directory.Exists(rootDir) == false) return;

string gaiaPath = System.IO.Path.Combine(rootDir, "GAIA\\");
string galexPath = System.IO.Path.Combine(rootDir, "Galex\\");

Console.WriteLine("Importing GAIA Files.. at " + gaiaPath);

// read each file in the gaia folder
var gaiaFiles = Directory.GetFiles(gaiaPath, "*.csv", SearchOption.TopDirectoryOnly);

StringBuilder results = new StringBuilder();
results.AppendLine("FILE, GAIA ROW, GALEX ROW, GAIA RA, GALEX RA, GAIA DEC, GALEX DEC");

foreach (var gaiaFile in gaiaFiles)
{
    string fileNamePrefix = Path.GetFileName(gaiaFile.Substring(0, gaiaFile.LastIndexOf('_')));
    Console.WriteLine("Processing file " + fileNamePrefix);

    List<string> linesFromGaia = null;
    List<string> linesFromGalex = null;

    while (linesFromGaia == null || linesFromGalex == null)
    {
        try
        {
            linesFromGaia = File.ReadAllLines(gaiaFile).ToList();
            linesFromGalex = File.ReadAllLines(Path.Combine(galexPath, fileNamePrefix + "_Galex.csv")).ToList();
        }
        catch
        {
            Console.WriteLine($"There was a problem opening {gaiaFile}! Be sure that the file is not opened in excel!");
            Console.WriteLine("Close the file in excel and press any key to try again.");
            Console.ReadKey();
        }
    }

    linesFromGaia.RemoveAt(0); // remove header row
    linesFromGalex.RemoveAt(0);

    int gaiaRow = 2; // we need to start at row 2 becaue of 0 vs 1 array and excel, plus we delete the header row
    foreach (string gaiaLine in linesFromGaia)
    {
        int galexRow = 2;
        string[] gaiaSplit = gaiaLine.Split(',');
        string gaia_ra = gaiaSplit[GAIA_RA_COL];
        string gaia_dec = gaiaSplit[GAIA_DEC_COL];

        float gaia_ra_float = Convert.ToSingle(gaia_ra);
        float gaia_dec_float = Convert.ToSingle(gaia_dec);

        foreach(string galexLine in linesFromGalex)
        {
            string[] galexSplit = galexLine.Split(',');
            string galex_ra = galexSplit[GALEX_RA_COL];
            string galex_dec = galexSplit[GALEX_DEC_COL];

            float galex_ra_float = Convert.ToSingle(galex_ra);
            float galex_dec_float = Convert.ToSingle(galex_dec);

            if(AreApprox(galex_ra_float, gaia_ra_float, APPROX_DETLA) && AreApprox(galex_dec_float, gaia_dec_float, APPROX_DETLA))
            {
                //results.AppendLine($"gaia's ra {gaia_ra_float} && gaia's dec {gaia_dec_float} = galex's ra {galex_ra_float} && galex's dec {galex_dec_float}");
                results.AppendLine($"{fileNamePrefix},{gaiaRow},{galexRow},{gaia_ra},{galex_ra},{gaia_dec},{galex_dec}");
            }

            galexRow++;
        }

        gaiaRow++;
    }
}



if (results.Length <= 0)
    Console.WriteLine("No results found");
else
{
    Console.WriteLine("Reults");
    Console.WriteLine("-------------------------------------");
    Console.Write(results.ToString());

    File.WriteAllText(Path.Combine(rootDir, "similiar.csv"), results.ToString());
}


bool AreApprox(float a, float b, float delta)
{
    if (Math.Abs(a - b) < delta)
    {
        return true;
    }
    else
    {
        return false;
    }
}
