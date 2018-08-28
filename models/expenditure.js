var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var expenditureSchema = new Schema({
    constituency: {
        type: String,
        required: true,
    },
    expenditure: {
        type: Number,
        required: true
    }
}, { collection : 'LSexpenditure2014' }, {
    timestamps: false
});


var expenditure = mongoose.model('expenditure', expenditureSchema);

module.exports = expenditure;