var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var mapSchema = new Schema({
    name: {
        type: String,
        required: true
    },
    position: {
        lat: String,
        lng: String
    },
    compound: {
        type: Number,
        default: 0
    },
    frequency: {
        type: Number,
        required: true
    },
    word: {
        type: Array,
        required: true
    }
},  { collection : 'mapview' }, {
    timestamps: false
});


var mapview = mongoose.model('mapview', mapSchema);

module.exports = mapview;