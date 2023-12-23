import { AccountMonitor } from './account.monitor';
import { BinanceApiClient } from './binance.client';

async function main() {
	// load api keys from environment variables
	const apiKey = process.env.BINANCE_API_KEY as string;
	const apiSecret = process.env.BINANCE_API_SECRET as string;

	// creates the Binance client
	const binance = new BinanceApiClient(apiKey, apiSecret);

	// test endpoints
	// console.log(await binance.fetchAccountInfo());
	// console.log(await binance.fetchExchangeInfo());
	// console.log(await binance.fetchListenKey());
	console.log(await binance.fetchTrades("LINABUSD"));

	const accountMonitor = new AccountMonitor(binance);
	accountMonitor.start();
}

main().then(() => console.log('Execution started!'));
