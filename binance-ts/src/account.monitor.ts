import { BinanceApiClient } from './binance.client';
import { WebsocketHandler } from './websocket.handler';

export class AccountMonitor {
	private _wsHandler?: WebsocketHandler;

	constructor(private _client: BinanceApiClient) {}

	async start() {
		// get the listen key
		const data = await this._client.fetchListenKey();
		const listenKey = data["listenKey"];

		// creates the websocket handler
		this._wsHandler = new WebsocketHandler('AccountMonitor', this.handleMessage, true);

		// subscribe to user data
		this._wsHandler.subscribeToUserData(listenKey);
	}

	// handles incoming messages over the websocket
	handleMessage(json: Map<string, any>) {
		console.log(json);
	}
}
