/*
 * Javascript functions for implementing
 *
 *
 */

"use strict";

// toggle tickboxes with same class as source
function toggleTickboxes(source) {
    var checkboxes = document.getElementsByClassName(source.className);
    for (var i=0, n=checkboxes.length; i<n; i++) {
        checkboxes[i].checked = source.checked;
    }
}
