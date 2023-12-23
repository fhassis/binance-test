import { connected } from 'process';
import { WebSocket } from 'ws';

type MessageHandler = (msg: Map<string, any>) => void;

export class WebsocketHandler {
	private _closedByError = false;
	private _baseUrl: string;
	private readonly _reconnectTime = 5000; // miliseconds
	private _ws?: WebSocket = undefined;
	private _subscriptions = new Set<string>();

	constructor(private readonly taskName: string, private callback: MessageHandler, testnet = false) {
		this._baseUrl = testnet ? 'wss://testnet.binance.vision/ws' : 'wss://stream.binance.com:9443/ws';

		// starts the socket
		this.start();
	}

	start() {
		// creates the websocket and connects it
		console.log(`${this.taskName}: connecting to ${this._baseUrl}`);
		this._ws = new WebSocket(this._baseUrl);

		// configures websocket connection
		this._ws.onopen = () => {
			console.log(`${this.taskName}: websocket connected`);
			this._closedByError = false;
			this._sendSubscription(Array.from(this._subscriptions), true);
		};

		// configures websocket closure
		this._ws.onclose = () => {
			console.log(`${this.taskName}: websocket closed`);
			this._ws = undefined;
			if (this._closedByError) {
				console.log(`${this.taskName}: retrying in ${this._reconnectTime / 1000}s ...`);
				setTimeout(() => this.start(), this._reconnectTime);
			} else {
				this.start();
			}
		};

		// configures websocket error
		this._ws.onerror = (err) => {
			console.log(`${this.taskName}: websocket error: ${err.message}`);
			this._closedByError = true;
			this._ws = undefined;
		};

		// configures websocket message handling
		this._ws.onmessage = (msg) => {
			// parse the received message as json
			var json: Map<string, any> = JSON.parse(msg.data as string);

			// pass the massage to the callback handler
			this.callback(json);
		};
	}

	private _sendSubscription(streams: string[], isSubscribe: boolean) {
		if (this._ws) {
			const payload = JSON.stringify({
				method: isSubscribe ? 'SUBSCRIBE' : 'UNSUBSCRIBE',
				params: streams,
				id: Date.now(),
			});
			console.log(payload);
			this._ws.send(payload);
		} else {
			console.log('ERROR: websocket not able to subscribe');
		}
	}

	subscribeToUserData(listenKey: string) {
		// add item to the subscription list
		this._subscriptions.add(listenKey);

		// send a live subscription in the websocket if connected
		if (this._ws && this._ws.readyState == WebSocket.OPEN) {
			this._sendSubscription([listenKey], true);
		}
	}
}
