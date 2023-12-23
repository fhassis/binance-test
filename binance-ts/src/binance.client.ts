import { createHmac, Hmac } from 'crypto';
import fetch, { Headers } from 'node-fetch';

import { AccountResponse, TradesResponse, UserDataStreamResponse } from './typings';

export class BinanceApiClient {
	private headers: Headers;
	private hmac: Hmac;
	private baseUrl: string;

	constructor(apiKey: string, apiSecret: string, testnet = false) {
		this.headers = new Headers();
		this.headers.set('X-MBX-APIKEY', apiKey);
		this.hmac = createHmac('sha256', apiSecret);
		this.baseUrl = testnet ? 'https://testnet.binance.vision' : 'https://api.binance.com';
	}

	private _getTimestamp() {
		return Date.now().toString();
	}

	private async _sendRequest(method: string, path: string, params?: Record<string, string>): Promise<any> {
		// creates a query param object
		const queryParams = new URLSearchParams(params);

		// adds signature to the params
		if (params && 'timestamp' in params) {
			queryParams.set('signature', this.hmac.update(queryParams.toString()).digest('hex'));
		}

		// forms the final url
		const url = queryParams ? `${this.baseUrl}${path}?${queryParams.toString()}` : `${this.baseUrl}${path}`;

		// performs the request
		try {
			const response = await fetch(url, { method, headers: this.headers });
			const data = await response.json();
			if (response.status === 200) {
				return data;
			} else {
				throw new Error(JSON.stringify(data));
			}
		} catch (error) {
			throw new Error(error as string);
		}
	}

	public async fetchAccountInfo(): Promise<AccountResponse> {
		const params = { timestamp: this._getTimestamp() };
		return await this._sendRequest('GET', '/api/v3/account', params);
	}

	public async fetchExchangeInfo() {
		return await this._sendRequest('GET', '/api/v3/exchangeInfo');
	}

	public async fetchListenKey(): Promise<UserDataStreamResponse> {
		return await this._sendRequest('POST', '/api/v3/userDataStream');
	}

	public async fetchTrades(
		symbol: string,
		fromId?: number,
		startTime?: number,
		endTime?: number,
		limit?: number
	): Promise<Array<TradesResponse>> {
		let params: any = { symbol, timestamp: this._getTimestamp() };
		if (fromId) {
			params.set('fromId', fromId);
		}
		if (startTime) {
			params.set('startTime', startTime);
		}
		if (endTime) {
			params.set('endTime', endTime);
		}
		if (limit) {
			params.set('limit', limit);
		}
		return await this._sendRequest('GET', '/api/v3/myTrades', params);
	}
}
