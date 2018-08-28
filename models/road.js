var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var introSchema = new Schema({
    ward: {
        type: String,
        required: true
    },
    humidity: {
        type: Number
    },
    rainfall: {
        type: Number
    },
    lat: {
        type: String
    },
    lng: {
        type: String
    },
    alarm: {
    	type: String
    },
    time : {
        type: String
    }

},  { collection : 'road' }, {
    timestamps: false
});


var road = mongoose.model('road', introSchema);

module.exports = road;