(function(){var t,e=this,i=e.Backbone;t="undefined"!=typeof exports?exports:e.Backbone={},t.VERSION="0.5.3";var r=e._;r||"undefined"==typeof require||(r=require("underscore")._);var s=e.jQuery||e.Zepto;t.noConflict=function(){return e.Backbone=i,this},t.emulateHTTP=!1,t.emulateJSON=!1,t.Events={bind:function(t,e,i){var r=this._callbacks||(this._callbacks={}),s=r[t]||(r[t]=[]);return s.push([e,i]),this},unbind:function(t,e){var i;if(t){if(i=this._callbacks)if(e){var r=i[t];if(!r)return this;for(var s=0,n=r.length;n>s;s++)if(r[s]&&e===r[s][0]){r[s]=null;break}}else i[t]=[]}else this._callbacks={};return this},trigger:function(t){var e,i,r,s,n,o=2;if(!(i=this._callbacks))return this;for(;o--;)if(r=o?t:"all",e=i[r])for(var a=0,h=e.length;h>a;a++)(s=e[a])?(n=o?Array.prototype.slice.call(arguments,1):arguments,s[0].apply(s[1]||this,n)):(e.splice(a,1),a--,h--);return this}},t.Model=function(t,e){var i;t||(t={}),(i=this.defaults)&&(r.isFunction(i)&&(i=i.call(this)),t=r.extend({},i,t)),this.attributes={},this._escapedAttributes={},this.cid=r.uniqueId("c"),this.set(t,{silent:!0}),this._changed=!1,this._previousAttributes=r.clone(this.attributes),e&&e.collection&&(this.collection=e.collection),this.initialize(t,e)},r.extend(t.Model.prototype,t.Events,{_previousAttributes:null,_changed:!1,idAttribute:"id",initialize:function(){},toJSON:function(){return r.clone(this.attributes)},get:function(t){return this.attributes[t]},escape:function(t){var e;if(e=this._escapedAttributes[t])return e;var i=this.attributes[t];return this._escapedAttributes[t]=x(null==i?"":""+i)},has:function(t){return null!=this.attributes[t]},set:function(t,e){if(e||(e={}),!t)return this;t.attributes&&(t=t.attributes);var i=this.attributes,s=this._escapedAttributes;if(!e.silent&&this.validate&&!this._performValidation(t,e))return!1;this.idAttribute in t&&(this.id=t[this.idAttribute]);var n=this._changing;this._changing=!0;for(var o in t){var a=t[o];r.isEqual(i[o],a)||(i[o]=a,delete s[o],this._changed=!0,e.silent||this.trigger("change:"+o,this,a,e))}return n||e.silent||!this._changed||this.change(e),this._changing=!1,this},unset:function(t,e){if(!(t in this.attributes))return this;e||(e={});var i=(this.attributes[t],{});return i[t]=void 0,e.silent||!this.validate||this._performValidation(i,e)?(delete this.attributes[t],delete this._escapedAttributes[t],t==this.idAttribute&&delete this.id,this._changed=!0,e.silent||(this.trigger("change:"+t,this,void 0,e),this.change(e)),this):!1},clear:function(t){t||(t={});var e,i=this.attributes,r={};for(e in i)r[e]=void 0;if(!t.silent&&this.validate&&!this._performValidation(r,t))return!1;if(this.attributes={},this._escapedAttributes={},this._changed=!0,!t.silent){for(e in i)this.trigger("change:"+e,this,void 0,t);this.change(t)}return this},fetch:function(e){e||(e={});var i=this,r=e.success;return e.success=function(t,s,n){return i.set(i.parse(t,n),e)?void(r&&r(i,t)):!1},e.error=w(e.error,i,e),(this.sync||t.sync).call(this,"read",this,e)},save:function(e,i){if(i||(i={}),e&&!this.set(e,i))return!1;var r=this,s=i.success;i.success=function(t,e,n){return r.set(r.parse(t,n),i)?void(s&&s(r,t,n)):!1},i.error=w(i.error,r,i);var n=this.isNew()?"create":"update";return(this.sync||t.sync).call(this,n,this,i)},destroy:function(e){if(e||(e={}),this.isNew())return this.trigger("destroy",this,this.collection,e);var i=this,r=e.success;return e.success=function(t){i.trigger("destroy",i,i.collection,e),r&&r(i,t)},e.error=w(e.error,i,e),(this.sync||t.sync).call(this,"delete",this,e)},url:function(){var t=y(this.collection)||this.urlRoot||b();return this.isNew()?t:t+("/"==t.charAt(t.length-1)?"":"/")+encodeURIComponent(this.id)},parse:function(t,e){return t},clone:function(){return new this.constructor(this)},isNew:function(){return null==this.id},change:function(t){this.trigger("change",this,t),this._previousAttributes=r.clone(this.attributes),this._changed=!1},hasChanged:function(t){return t?this._previousAttributes[t]!=this.attributes[t]:this._changed},changedAttributes:function(t){t||(t=this.attributes);var e=this._previousAttributes,i=!1;for(var s in t)r.isEqual(e[s],t[s])||(i=i||{},i[s]=t[s]);return i},previous:function(t){return t&&this._previousAttributes?this._previousAttributes[t]:null},previousAttributes:function(){return r.clone(this._previousAttributes)},_performValidation:function(t,e){var i=this.validate(t);return i?(e.error?e.error(this,i,e):this.trigger("error",this,i,e),!1):!0}}),t.Collection=function(t,e){e||(e={}),e.comparator&&(this.comparator=e.comparator),r.bindAll(this,"_onModelEvent","_removeReference"),this._reset(),t&&this.reset(t,{silent:!0}),this.initialize.apply(this,arguments)},r.extend(t.Collection.prototype,t.Events,{model:t.Model,initialize:function(){},toJSON:function(){return this.map(function(t){return t.toJSON()})},add:function(t,e){if(r.isArray(t))for(var i=0,s=t.length;s>i;i++)this._add(t[i],e);else this._add(t,e);return this},remove:function(t,e){if(r.isArray(t))for(var i=0,s=t.length;s>i;i++)this._remove(t[i],e);else this._remove(t,e);return this},get:function(t){return null==t?null:this._byId[null!=t.id?t.id:t]},getByCid:function(t){return t&&this._byCid[t.cid||t]},at:function(t){return this.models[t]},sort:function(t){if(t||(t={}),!this.comparator)throw new Error("Cannot sort a set without a comparator");return this.models=this.sortBy(this.comparator),t.silent||this.trigger("reset",this,t),this},pluck:function(t){return r.map(this.models,function(e){return e.get(t)})},reset:function(t,e){return t||(t=[]),e||(e={}),this.each(this._removeReference),this._reset(),this.add(t,{silent:!0}),e.silent||this.trigger("reset",this,e),this},fetch:function(e){e||(e={});var i=this,r=e.success;return e.success=function(t,s,n){i[e.add?"add":"reset"](i.parse(t,n),e),r&&r(i,t)},e.error=w(e.error,i,e),(this.sync||t.sync).call(this,"read",this,e)},create:function(t,e){var i=this;if(e||(e={}),t=this._prepareModel(t,e),!t)return!1;var r=e.success;return e.success=function(t,s,n){i.add(t,e),r&&r(t,s,n)},t.save(null,e),t},parse:function(t,e){return t},chain:function(){return r(this.models).chain()},_reset:function(t){this.length=0,this.models=[],this._byId={},this._byCid={}},_prepareModel:function(e,i){if(e instanceof t.Model)e.collection||(e.collection=this);else{var r=e;e=new this.model(r,{collection:this}),e.validate&&!e._performValidation(r,i)&&(e=!1)}return e},_add:function(t,e){if(e||(e={}),t=this._prepareModel(t,e),!t)return!1;var i=this.getByCid(t);if(i)throw new Error(["Can't add the same model to a set twice",i.id]);this._byId[t.id]=t,this._byCid[t.cid]=t;var r=null!=e.at?e.at:this.comparator?this.sortedIndex(t,this.comparator):this.length;return this.models.splice(r,0,t),t.bind("all",this._onModelEvent),this.length++,e.silent||t.trigger("add",t,this,e),t},_remove:function(t,e){return e||(e={}),(t=this.getByCid(t)||this.get(t))?(delete this._byId[t.id],delete this._byCid[t.cid],this.models.splice(this.indexOf(t),1),this.length--,e.silent||t.trigger("remove",t,this,e),this._removeReference(t),t):null},_removeReference:function(t){this==t.collection&&delete t.collection,t.unbind("all",this._onModelEvent)},_onModelEvent:function(t,e,i,r){("add"!=t&&"remove"!=t||i==this)&&("destroy"==t&&this._remove(e,r),e&&t==="change:"+e.idAttribute&&(delete this._byId[e.previous(e.idAttribute)],this._byId[e.id]=e),this.trigger.apply(this,arguments))}});var n=["forEach","each","map","reduce","reduceRight","find","detect","filter","select","reject","every","all","some","any","include","contains","invoke","max","min","sortBy","sortedIndex","toArray","size","first","rest","last","without","indexOf","lastIndexOf","isEmpty","groupBy"];r.each(n,function(e){t.Collection.prototype[e]=function(){return r[e].apply(r,[this.models].concat(r.toArray(arguments)))}}),t.Router=function(t){t||(t={}),t.routes&&(this.routes=t.routes),this._bindRoutes(),this.initialize.apply(this,arguments)};var o=/:([\w\d]+)/g,a=/\*([\w\d]+)/g,h=/[-[\]{}()+?.,\\^$|#\s]/g;r.extend(t.Router.prototype,t.Events,{initialize:function(){},route:function(e,i,s){t.history||(t.history=new t.History),r.isRegExp(e)||(e=this._routeToRegExp(e)),t.history.route(e,r.bind(function(t){var r=this._extractParameters(e,t);s.apply(this,r),this.trigger.apply(this,["route:"+i].concat(r))},this))},navigate:function(e,i){t.history.navigate(e,i)},_bindRoutes:function(){if(this.routes){var t=[];for(var e in this.routes)t.unshift([e,this.routes[e]]);for(var i=0,r=t.length;r>i;i++)this.route(t[i][0],t[i][1],this[t[i][1]])}},_routeToRegExp:function(t){return t=t.replace(h,"\\$&").replace(o,"([^/]*)").replace(a,"(.*?)"),new RegExp("^"+t+"$")},_extractParameters:function(t,e){return t.exec(e).slice(1)}}),t.History=function(){this.handlers=[],r.bindAll(this,"checkUrl")};var u=/^#*/,c=/msie [\w.]+/,l=!1;r.extend(t.History.prototype,{interval:50,getFragment:function(t,e){if(null==t)if(this._hasPushState||e){t=window.location.pathname;var i=window.location.search;i&&(t+=i),0==t.indexOf(this.options.root)&&(t=t.substr(this.options.root.length))}else t=window.location.hash;return decodeURIComponent(t.replace(u,""))},start:function(t){if(l)throw new Error("Backbone.history has already been started");this.options=r.extend({},{root:"/"},this.options,t),this._wantsPushState=!!this.options.pushState,this._hasPushState=!!(this.options.pushState&&window.history&&window.history.pushState);var e=this.getFragment(),i=document.documentMode,n=c.exec(navigator.userAgent.toLowerCase())&&(!i||7>=i);n&&(this.iframe=s('<iframe src="javascript:0" tabindex="-1" />').hide().appendTo("body")[0].contentWindow,this.navigate(e)),this._hasPushState?s(window).bind("popstate",this.checkUrl):"onhashchange"in window&&!n?s(window).bind("hashchange",this.checkUrl):setInterval(this.checkUrl,this.interval),this.fragment=e,l=!0;var o=window.location,a=o.pathname==this.options.root;return!this._wantsPushState||this._hasPushState||a?(this._wantsPushState&&this._hasPushState&&a&&o.hash&&(this.fragment=o.hash.replace(u,""),window.history.replaceState({},document.title,o.protocol+"//"+o.host+this.options.root+this.fragment)),this.options.silent?void 0:this.loadUrl()):(this.fragment=this.getFragment(null,!0),window.location.replace(this.options.root+"#"+this.fragment),!0)},route:function(t,e){this.handlers.unshift({route:t,callback:e})},checkUrl:function(t){var e=this.getFragment();return e==this.fragment&&this.iframe&&(e=this.getFragment(this.iframe.location.hash)),e==this.fragment||e==decodeURIComponent(this.fragment)?!1:(this.iframe&&this.navigate(e),void(this.loadUrl()||this.loadUrl(window.location.hash)))},loadUrl:function(t){var e=this.fragment=this.getFragment(t),i=r.any(this.handlers,function(t){return t.route.test(e)?(t.callback(e),!0):void 0});return i},navigate:function(t,e){var i=(t||"").replace(u,"");if(this.fragment!=i&&this.fragment!=decodeURIComponent(i)){if(this._hasPushState){var r=window.location;0!=i.indexOf(this.options.root)&&(i=this.options.root+i),this.fragment=i,window.history.pushState({},document.title,r.protocol+"//"+r.host+i)}else window.location.hash=this.fragment=i,this.iframe&&i!=this.getFragment(this.iframe.location.hash)&&(this.iframe.document.open().close(),this.iframe.location.hash=i);e&&this.loadUrl(t)}}}),t.View=function(t){this.cid=r.uniqueId("view"),this._configure(t||{}),this._ensureElement(),this.delegateEvents(),this.initialize.apply(this,arguments)};var d=function(t){return s(t,this.el)},f=/^(\S+)\s*(.*)$/,p=["model","collection","el","id","attributes","className","tagName"];r.extend(t.View.prototype,t.Events,{tagName:"div",$:d,initialize:function(){},render:function(){return this},remove:function(){return s(this.el).remove(),this},make:function(t,e,i){var r=document.createElement(t);return e&&s(r).attr(e),i&&s(r).html(i),r},delegateEvents:function(t){if(t||(t=this.events)){r.isFunction(t)&&(t=t.call(this)),s(this.el).unbind(".delegateEvents"+this.cid);for(var e in t){var i=this[t[e]];if(!i)throw new Error('Event "'+t[e]+'" does not exist');var n=e.match(f),o=n[1],a=n[2];i=r.bind(i,this),o+=".delegateEvents"+this.cid,""===a?s(this.el).bind(o,i):s(this.el).delegate(a,o,i)}}},_configure:function(t){this.options&&(t=r.extend({},this.options,t));for(var e=0,i=p.length;i>e;e++){var s=p[e];t[s]&&(this[s]=t[s])}this.options=t},_ensureElement:function(){if(this.el)r.isString(this.el)&&(this.el=s(this.el).get(0));else{var t=this.attributes||{};this.id&&(t.id=this.id),this.className&&(t["class"]=this.className),this.el=this.make(this.tagName,t)}}});var g=function(t,e){var i=_(this,t,e);return i.extend=this.extend,i};t.Model.extend=t.Collection.extend=t.Router.extend=t.View.extend=g;var v={create:"POST",update:"PUT","delete":"DELETE",read:"GET"};t.sync=function(e,i,n){var o=v[e],a=r.extend({type:o,dataType:"json"},n);return a.url||(a.url=y(i)||b()),a.data||!i||"create"!=e&&"update"!=e||(a.contentType="application/json",a.data=JSON.stringify(i.toJSON())),t.emulateJSON&&(a.contentType="application/x-www-form-urlencoded",a.data=a.data?{model:a.data}:{}),t.emulateHTTP&&("PUT"===o||"DELETE"===o)&&(t.emulateJSON&&(a.data._method=o),a.type="POST",a.beforeSend=function(t){t.setRequestHeader("X-HTTP-Method-Override",o)}),"GET"===a.type||t.emulateJSON||(a.processData=!1),s.ajax(a)};var m=function(){},_=function(t,e,i){var s;return s=e&&e.hasOwnProperty("constructor")?e.constructor:function(){return t.apply(this,arguments)},r.extend(s,t),m.prototype=t.prototype,s.prototype=new m,e&&r.extend(s.prototype,e),i&&r.extend(s,i),s.prototype.constructor=s,s.__super__=t.prototype,s},y=function(t){return t&&t.url?r.isFunction(t.url)?t.url():t.url:null},b=function(){throw new Error('A "url" property or function must be specified')},w=function(t,e,i){return function(r){t?t(e,r,i):e.trigger("error",e,r,i)}},x=function(t){return t.replace(/&(?!\w+;|#\d+;|#x[\da-f]+;)/gi,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#x27;").replace(/\//g,"&#x2F;")}}).call(this);
