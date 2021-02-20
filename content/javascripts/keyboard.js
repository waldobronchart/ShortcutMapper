

(function($) {
    "use strict";
    
    $.widget("custom.keyboard", {

        options: {
            keydata: {},
            mods: [],
            context: 0
        },

        activeModKeys: [],
        contextItems: null,
        highlightedKeyName: null,
        standardModClasses: ["nomod", "alt", "command", "control", "shift", "multi", "other"],

        _create: function() {
            var keyboard = this;

            // Initialize Buttons and insert all context data
            var buttons = this.element.find("button");
            buttons.each(function() {
                var html = "<span class='label'>" + $(this).text() + "</span><b></b>";
                var keyName = $(this).data("key");
                var hasShortcut = false;

                for (var contextName in keyboard.options.keydata) {
                    if (!keyboard.options.keydata.hasOwnProperty(contextName)) {
                        continue;
                    }
                        
                    var context = keyboard.options.keydata[contextName];
                    var contextSafeName = keyboard._getSafeID(contextName);
                    var keyItems = context[keyName];

                    if (keyItems) {
                        html += "<div class='keyitems' data-context='" + contextSafeName + "'>";

                        for (var i=0; i<keyItems.length; i++) {
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
                if (!hasShortcut) {
                    $(this).addClass("unmapped");
                }

                // Is key a modifier key?
                if ($.inArray(keyName, keyboard.options.mods) >= 0) {
                    // This css class gives the mod a colored border
                    $(this).addClass("mod-" + keyboard._getButtonModClass(keyName));

                    // Click to toggle modifier activeness
                    $(this).on("click", function() {
                        if ($.inArray(keyName, keyboard.activeModKeys) >= 0) {
                            keyboard._deactivateModifiers([keyName]);
                        } else {
                            keyboard._activateModifiers([keyName]);
                        }
                    });
                }
            });

            // Set context
            this.switchContext(keyboard.options.context);

            // Register key events
            $(document).on("keydown", null, $.proxy(this._keyDown, this));
            $(document).on("keyup", null, $.proxy(this._keyUp, this));
            this._clearActiveModifiers();
            this._update();
        },

        _keyDown: function(e) {
            var keyName = window.utils.keyCodeMap[e.which];

            // Is key a modifier key?
            if ($.inArray(keyName, this.options.mods) >= 0) {
                e.preventDefault();
            }

            // Escape key clears all modifier activeness
            if (keyName === "ESCAPE") {
                this._clearActiveModifiers();
                this._update();
                return;
            }

            this._activateModifiers([keyName]);
        },

        _keyUp: function(e) {
            var keyName = window.utils.keyCodeMap[e.which];

            // Is key a modifier key?
            if ($.inArray(keyName, this.options.mods) >= 0) {
                e.preventDefault();
            }

            this._deactivateModifiers([keyName]);
        },

        _activateModifiers: function(modKeyNames) {
            for (var i=0; i<modKeyNames.length; i++) {
                var keyName = modKeyNames[i];
                if ($.inArray(keyName, this.options.mods) < 0) {
                    return;
                }
                if ($.inArray(keyName, this.activeModKeys) >= 0) {
                    return;
                }

                // Add activeness class from mod buttons
                var modClass = "mod-" + this._getButtonModClass(keyName);
                $(this.element).find("button." + modClass).addClass("mod-active");

                // Add to active modifier key list
                this.activeModKeys.push(keyName);
            }

            this._update();
        },

        _deactivateModifiers: function(modKeyNames) {
            for (var i=0; i<modKeyNames.length; i++) {
                var keyName = modKeyNames[i];
                if ($.inArray(keyName, this.options.mods) < 0) {
                    return;
                }
                if ($.inArray(keyName, this.activeModKeys) < 0) {
                    return;
                }

                // Remove activeness class from mod buttons
                var modClass = "mod-" + this._getButtonModClass(keyName);
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
            if (this.highlightedKeyName === null) {
                return;
            }

            this.highlightedKeyName = null;
            this._update();
        },

        _getButtonModClass: function(keyName) {
            var keyNameLower = keyName.toLowerCase();
            if ($.inArray(keyNameLower, this.standardModClasses) >= 0) {
                return keyNameLower;
            }

            return "other";
        },

        _update: function() {
            var mods = "NOMOD";
            if (this.activeModKeys.length > 0) {
                mods = this.activeModKeys.sort().join("_");
            }

            var inHighlightMode = (this.highlightedKeyName !== null);
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
            this.element.find("button").removeClass(this.standardModClasses.join(" "));

            // Highlight keys
            var buttonModClass = "nomod";
            if (this.activeModKeys.length === 1) {
                buttonModClass = this._getButtonModClass(this.activeModKeys[0]);
            }
            if (this.activeModKeys.length > 1) {
                buttonModClass = "multi";
            }
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
            $(document).off("keyup", null, this._keyUp);
        }
    });
})(jQuery);
