var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var tSchema = new Schema({
    date: {
        type: Number
    }
},  { collection : 'timeline' }, {
    timestamps: false
});


var to30 = mongoose.model('timeline', tSchema);

module.exports = to30;