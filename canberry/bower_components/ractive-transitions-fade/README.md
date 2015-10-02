# ractive-transitions-fade

*Find more Ractive.js plugins at [ractivejs.org/plugins](http://ractivejs.org/plugins)*

This transition fades an element in and out of view, using CSS transitions where possible.

```html
{{#if visible}}
  <div intro-outro='fade'>
    this will fade in and out of view
    depending on the value of `visible`
  </div>
{{/if}}
```

## Installation

Install from npm...

```bash
npm install ractive-transitions-fade
```

...or download it and add it as a script tag to your page:

```html
<script src='ractive.js'></script> <!-- must go first! -->
<script src='ractive-transitions-fade.js'></script>
```

## Use as a module...

*Note: previous versions of this plugin would 'self-register'. If you are using a module system such as Browserify, Webpack or RequireJS, that's no longer the case - you must explicitly register the plugin.*


### CommonJS

```js
var Ractive = require( 'ractive' );

// To use the fade transition with a specific instance
var ractive = new Ractive({
  el: 'body',
  template: myTemplate,
  transitions: {
    fade: require( 'ractive-transitions-fade' )
  }
});

// To use it with components
MyComponent = Ractive.extend({
  template: componentTemplate,
  transitions: {
    fade: require( 'ractive-transitions-fade' )
  }
});

// To make it globally available to *all* instances
Ractive.transitions.fade = require( 'ractive-transitions-fade' );
```


### AMD

```js
define([ 'ractive', 'ractive-transitions-fade' ], function ( Ractive, fade ) {
  var ractive = new Ractive({
    el: 'body',
    template: myTemplate,
    transitions: {
      fade: fade
    }
  });
});
```


### ES6

```js
import Ractive from 'ractive';

var ractive = new Ractive({
  el: 'body',
  template: myTemplate,
  transitions: { fade }
});
```


## Use as a `<script>` tag

If you include ractive-transitions-fade as a script tag, it will 'self-register' with the global `Ractive` object, and all Ractive instances will be able to use it.



## Parameters

You can specify the `delay`, `duration` and `easing` parameters using the conventional syntax:

```html
<div intro='fade:{"delay":500,"duration":500}'>content</div>
```

Both `delay` and `duration` are in milliseconds. The `easing` value must be a valid CSS easing function (see http://cubic-bezier.com/).



## License

Copyright (c) 2013-15 Rich Harris. Licensed MIT.
