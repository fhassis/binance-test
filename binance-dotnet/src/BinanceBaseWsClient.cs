using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

class BinanceBaseWsClient
{
    private readonly ClientWebSocket ws;
    private readonly string baseUrl;
    private readonly int BUFFER_SIZE = 4096;
    private readonly JsonSerializerOptions serializerOptions;

    public BinanceBaseWsClient(string baseUrl)
    {
        ws = new ClientWebSocket();
        this.baseUrl = baseUrl;
        serializerOptions = new JsonSerializerOptions
        {
            DictionaryKeyPolicy = JsonNamingPolicy.CamelCase,
            NumberHandling = JsonNumberHandling.AllowReadingFromString
        };
    }


    protected async IAsyncEnumerable<T> Stream<T>(string subscriptionString)
    {
        // create the final url string
        string url = $"{baseUrl}/ws/{subscriptionString}";

        // connects to the server
        await ws.ConnectAsync(new Uri(url), CancellationToken.None);

        // handles messages receiving
        var buffer = new byte[BUFFER_SIZE];
        while (ws.State == WebSocketState.Open)
        {
            // waits for messages from the server
            var result = await ws.ReceiveAsync(buffer, CancellationToken.None);

            // check the type of message received
            if (result.MessageType == WebSocketMessageType.Close)
            {
                // closes the connection
                await ws.CloseAsync(WebSocketCloseStatus.NormalClosure, null, CancellationToken.None);
            }
            else
            {
                // converts the buffer to a string
                var jsonString = Encoding.UTF8.GetString(buffer, 0, result.Count);

                System.Console.WriteLine(jsonString);

                // deserialize the json object
                var parsedObject = JsonSerializer.Deserialize<T>(jsonString, serializerOptions) ?? throw new Exception($"Unable to convert the following json:\n{jsonString}");

                // returns the received data
                yield return parsedObject;
            }
        }
    }
}
