

(function($) {
    $.widget("custom.keyboard", {

        options: {
            keydata: {},
            mods: [],
            context: 0
        },

        keyCodeMap: {
            8:"BACKSPACE", 9:"TAB", 13:"RETURN", 16:"SHIFT", 17:"CONTROL", 18:"ALT", 19:"PAUSEBREAK", 20:"CAPSLOCK",
            27:"ESCAPE", 32:"SPACE", 33:"PAGEUP", 34:"PAGEDOWN", 35:"END", 36:"HOME", 37:"LEFT", 38:"UP", 39:"RIGHT",
            40:"DOWN", 43:"PLUS", 44:"PRINTSCREEN", 45:"INSERT", 46:"DELETE",
            48:"ZERO", 49:"ONE", 50:"TWO", 51:"THREE", 52:"FOUR", 53:"FIVE", 54:"SIX", 55:"SEVEN", 56:"EIGHT", 57:"NINE",
            59:"SEMICOLON", 61:"EQUAL",
            65:"A", 66:"B", 67:"C", 68:"D", 69:"E", 70:"F", 71:"G", 72:"H", 73:"I", 74:"J", 75:"K", 76:"L",
            77:"M", 78:"N", 79:"O", 80:"P", 81:"Q", 82:"R", 83:"S", 84:"T", 85:"U", 86:"V", 87:"W", 88:"X", 89:"Y", 90:"Z",
            91:"COMMAND",
            96:"NUMPAD_ZERO", 97:"NUMPAD_ONE", 98:"NUMPAD_TWO", 99:"NUMPAD_THREE", 100:"NUMPAD_FOUR", 101:"NUMPAD_FIVE",
            102:"NUMPAD_SIX", 103:"NUMPAD_SEVEN", 104:"NUMPAD_EIGHT", 105:"NUMPAD_NINE",
            106: "NUMPAD_ASTERISK", 107:"NUMPAD_PLUS", 109:"NUMPAD_MINUS", 110:"NUMPAD_PERIOD", 111: "NUMPAD_SLASH",
            112:"F1", 113:"F2", 114:"F3", 115:"F4", 116:"F5", 117:"F6", 118:"F7", 119:"F8", 120:"F9", 121:"F10", 122:"F11", 123:"F12",
            144:"NUMLOCK", 145:"SCROLLLOCK", 186:"SEMICOLON", 187:"NUMPAD_EQUAL", 188:"COMMA", 189:"MINUS", 190:"PERIOD", 191:"SLASH", 192:"ACCENT_GRAVE",
            219:"LEFT_BRACKET", 220:"BACKSLASH", 221:"RIGHT_BRACKET", 222:"SINGLE_QOUTE"
        },

        activeModKeys: [],
        contextItems: null,
        highlightedKeyName: null,

        _create: function() {
            var keyboard = this;

            // Initialize Buttons and insert all context data
            var buttons = this.element.find("button");
            buttons.each(function() {
                var html = "<span class='label'>" + $(this).text() + "</span><b></b>";
                var keyName = $(this).data("key");
                var hasShortcut = false;

                for (var contextName in keyboard.options.keydata) {
                    var context = keyboard.options.keydata[contextName];
                    var contextSafeName = keyboard._getSafeID(contextName);
                    var keyItems = context[keyName];

                    if (keyItems) {
                        html += "<div class='keyitems' data-context='" + contextSafeName + "'>";

                        for (i=0; i<keyItems.length; i++) {
                            var keyItem = keyItems[i];
                            var mods = (keyItem.mods.length > 0) ? keyItem.mods.join('_') : "NOMOD";
                            html += "<div class='shortcut' data-mods='" + mods + "'>" + keyItem.name + "</div>";
                        }

                        html += "</div>";

                        hasShortcut = true;
                    }
                }

                $(this).html(html);

                // Is this key ever used?
                if (!hasShortcut)
                    $(this).addClass("unmapped");

                // Is key a modifier key?
                if ($.inArray(keyName, keyboard.options.mods) >= 0) {
                    var modClass = "mod-" + keyName.toLowerCase();
                    $(this).addClass(modClass);

                    // Click to toggle modifier activeness
                    $(this).on("click", function() {
                        if ($.inArray(keyName, keyboard.activeModKeys) >= 0)
                            keyboard._deactivateModifiers([keyName]);
                        else
                            keyboard._activateModifiers([keyName]);
                    });
                }
            });

            // Set context
            this.switchContext(keyboard.options.context);

            // Register key events
            $(document).on("keydown", null, $.proxy(this._keyDown, this));
            $(document).on("keyup", null, $.proxy(this._keyUp, this));
        },

        _keyDown: function(e) {
            var keyName = this.keyCodeMap[e.which];

            // Escape key clears all modifier activeness
            if (keyName === "ESCAPE") {
                this._clearActiveModifiers();
                this._update();
                return;
            }

            this._activateModifiers([keyName]);
        },

        _keyUp: function(e) {
            var keyName = this.keyCodeMap[e.which];
            this._deactivateModifiers([keyName]);
        },

        _activateModifiers: function(modKeyNames) {
            for (i=0; i<modKeyNames.length; i++) {
                var keyName = modKeyNames[i];
                if ($.inArray(keyName, this.options.mods) < 0)
                    return;
                if ($.inArray(keyName, this.activeModKeys) >= 0)
                    return;

                // Add activeness class from mod buttons
                var modClass = "mod-" + keyName.toLowerCase();
                $(this.element).find("button." + modClass).addClass("mod-active");

                // Add to active modifier key list
                this.activeModKeys.push(keyName);
            }

            this._update();
        },

        _deactivateModifiers: function(modKeyNames) {
            for (i=0; i<modKeyNames.length; i++) {
                var keyName = modKeyNames[i];
                if ($.inArray(keyName, this.options.mods) < 0)
                    return;
                if ($.inArray(keyName, this.activeModKeys) < 0)
                    return;

                // Remove activeness class from mod buttons
                var modClass = "mod-" + keyName.toLowerCase();
                $(this.element).find("button." + modClass).removeClass("mod-active");

                // Remove from active modifier key
                var idx = this.activeModKeys.indexOf(keyName);
                this.activeModKeys.splice(idx, 1);
            }

            this._update();
        },

        _clearActiveModifiers: function() {
            this.activeModKeys = [];
            $(this.element).find("button.mod-active").removeClass("mod-active");
        },

        _getSafeID: function(name) {
            name = String(name);
            return name.replace(/ /g, "_").replace(/:/g, "").toUpperCase();
        },

        switchContext: function(name) {
            this.options.context = name;
            var contextSafeName = this._getSafeID(name);

            console.log("KEYBOARD switch context to " + name);

            // Cleanup and hide
            this.element.find("button").removeClass("hasitems");
            this.element.find("button div.keyitems").hide();

            // Show current context shortcuts
            this.contextItems = this.element.find("button div.keyitems[data-context='" + contextSafeName + "']");
            this.contextItems.closest("button").addClass("hasitems");
            this.contextItems.show();

            this._update();
        },

        setActiveMods: function(mods) {
            this._clearActiveModifiers();
            this._activateModifiers(mods);
        },

        highlightShortcut: function(keyName, shortcut) {
            this.setActiveMods(shortcut.mods);
            this.highlightedKeyName = keyName;
            this._update();
        },

        exitHighlightMode: function() {
            if (this.highlightedKeyName === null)
                return;

            this.highlightedKeyName = null;
            this._update();
        },

        _update: function() {
            var mods = "NOMOD";
            if (this.activeModKeys.length > 0)
                mods = this.activeModKeys.sort().join("_");

            var inHighlightMode = (this.highlightedKeyName != null);
            var buttonSelector = "button" + ((inHighlightMode) ? "[data-key='" + this.highlightedKeyName + "']" : "");

            // Show only shortcut labels from current mods
            if (inHighlightMode) {
                this.contextItems.children().hide();
                var c = this._getSafeID(this.options.context);
                $(this.element).find(buttonSelector + " div.keyitems[data-context='" + c + "'] div.shortcut[data-mods='" + mods + "']").show();
            } else {
                this.contextItems.children().show();
                this.contextItems.children("div.shortcut[data-mods!='" + mods + "']").hide();
            }

            // Clear all button highlight state
            var standardModClasses = ["nomod", "alt", "command", "control", "shift", "multi"];
            this.element.find("button").removeClass(standardModClasses.join(" "));

            // Highlight keys
            var buttonModClass = "nomod";
            if (this.activeModKeys.length == 1)
                buttonModClass = this.activeModKeys[0].toLowerCase();
            if (this.activeModKeys.length > 1)
                buttonModClass = "multi";
            this.contextItems.children("div.shortcut[data-mods='" + mods + "']").closest(buttonSelector).addClass(buttonModClass);
        },

        _setOption: function(key, value) {
            this.options[key] = value;

            switch(key) {
                case "context":
                    this.switchContext(value);
                    break;
            }

            this._super("_setOption", key, value);
        },

        _destroy: function() {
            // Deregister key events
            $(document).off("keydown", null, this._keyDown);
            $(document).off("keyup", null, this._keyDown);
        }
    });
})(jQuery);
