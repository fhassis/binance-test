typedef Json = Map<String, dynamic>;

enum Timeframe { m1, m15, m30, h1, h4, d1, w1 }

/// extension to add a conversion of timeframe to string
extension TfToSting on Timeframe {
  String toBinanceString() {
    switch (this) {
      case Timeframe.h4:
        return '4h';
      case Timeframe.h1:
        return '1h';
      case Timeframe.d1:
        return '1d';
      case Timeframe.m30:
        return '30m';
      case Timeframe.m15:
        return '15m';
      case Timeframe.m1:
        return '1m';
      default:
        throw UnimplementedError('Invalid Timeframe: $this');
    }
  }
}

class Candle {
  final int time;
  final double open;
  final double high;
  final double low;
  final double close;
  final double volume;

  Candle({
    required this.time,
    required this.open,
    required this.high,
    required this.low,
    required this.close,
    required this.volume,
  });
}
