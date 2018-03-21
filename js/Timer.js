// 定时器类

function Timer(){
    this.initialize.apply(this, arguments);
}
 
Timer.prototype =  {
    _callback: null,
    _start: 0,
    _interval1: 0,
    _interval2: 0,
    _first_tick: true,
    _tid: 0,
    _last_delay: 0,

    /*
          初始化
          @param callback: function，timer触发时的回调函数
          @param start: int；毫秒；第一次运行时的间隔，如果此参数不存在或小于等于0，callback会立即执行。
          @param interval1: int；毫秒；第一次以后每次的间隔（最小），如果此参数不存在，则第一次timeout后就退出定时
          @param interval2: int；毫秒；第一次以后每次的间隔（最大），如果此参数存在，则会在[interval1, interval2]范围内随机一个时间
    */
    initialize: function(callback, start, interval1, interval2) {
        this._callback = callback;
        this._start = start ? start : 0;
        this._interval1 = interval1 ? interval1 : 0;
        this._interval2 = interval2 ? interval2 : this._interval1;
    },
    _on_timeout: function() {
        this._first_tick = false;
        console.log(this);
        this._callback();
        if (this._interval1 > 0) {
            var _this = this;
            this._tid = setTimeout( function () {
                _this._on_timeout();
            }, this.delay() );
        }
    },
    delay: function() {
        this._last_delay = this._first_tick ? this._start : parseInt(Math.random()*(this._interval2 - this._interval1 + 1) + this._interval1, 10);
        return this._last_delay;
    },
    start: function(reset_to_first_tick) {
        if (reset_to_first_tick)
            this._first_tick = true;
        
        if (this._start <= 0)
            this._on_timeout();
        else {
            var _this = this;
            this._tid = setTimeout( function () {
                _this._on_timeout();
            }, this.delay() );
        }
    },
    stop: function() {
        clearTimeout(this._tid);
    }

}; 