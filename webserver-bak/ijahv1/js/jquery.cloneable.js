/**
 * @author Alexander Chuprin a.s.chuprin@gmail.com
 * @since 20.08.11
 */
(function($) {
    $.fn.cloneable = function(options) {
        var defaults = {
            before: $.noop,
            after: $.noop,
            copies: 1
        };

        var settings = $.extend({}, defaults, options);

        return this.each(function() {
            var self = $(this);
            var counter = 0;
            var original = self.clone();
            var addButton = $('<span class="jc-add">add</span>');

            /* Append clone button */
            self.append(addButton);

            addButton.click(function(){
                for (var i = 0; i < settings.copies; i++) {
                    settings.before.call(original);

                    var clone = original.clone();
                    var removeButton = $('<span class="jc-remove">remove</span>');

                    removeButton.click(function() {
                        clone.remove();
                    });

                    clone.insertAfter(self)
                        .find('[id]') // We should update all IDs.
                        .andSelf()
                        .attr('id', function(index, val) {
                            if (val) {
                                var newId = val + counter;
                                clone.find('label').filter('[for=' + val + ']').attr('for', newId); // Also update label associated with old ID.
                                return newId;
                            }
                        })
                        .cloneable(settings) // Make cloneable just cloned block also.
                        .append(removeButton);

                    /* Reset all input values */
                    clone.find(':input:not(select)').val('');
                    clone.find('select option:first').attr('selected', 'selected');

                    counter++;
                    settings.after.call(clone);
                }
            });
        });
    };
})(jQuery)