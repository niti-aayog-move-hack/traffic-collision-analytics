var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var top30Schema = new Schema({
    frequency: {
        type: Number
    }
}, {
    timestamps: false
});


var top30 = mongoose.model('top30', top30Schema);

module.exports = top30;