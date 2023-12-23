export interface ServerTimeResponse {
	serverTime: number;
}

export interface BalanceResponse {
	asset: string;
	free: string;
	locked: string;
}

export interface AccountResponse {
	makerCommission: number;
	takerCommission: number;
	buyerCommission: number;
	sellerCommission: number;
	canTrade: boolean;
	canWithdraw: boolean;
	canDeposit: boolean;
	updateTime: number;
	accountType: string;
	balances: Array<BalanceResponse>;
	permissions: Array<string>;
}

export interface TradesResponse {
	symbol: string;
	id: number;
	orderId: number;
	orderListId: number;
	price: string;
	qty: string;
	quoteQty: string;
	commission: string;
	commissionAsset: string;
	time: number;
	isBuyer: boolean;
	isMaker: boolean;
	isBestMatch: boolean;
}

export interface UserDataStreamResponse {
	listenKey: string;
}
