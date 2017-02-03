function swapJsonKeyValues(input) {
    var one, output = {};
    for (one in input) {
        if (input.hasOwnProperty(one)) {
            output[input[one]] = one;
        }
    }
    return output;
}

var stateAbbrs = swapJsonKeyValues(States);