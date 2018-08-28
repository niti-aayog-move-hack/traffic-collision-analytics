var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var introSchema = new Schema({
    name: {
        type: String,
        required: true
    },
    positive: {
        type: Number
    },
    negative: {
        type: Number
    },
    intro: {
    	type: String
    },
    party : {
        type: String
    }
},  { collection : 'intro' }, {
    timestamps: false
});


var intro = mongoose.model('intro', introSchema);

module.exports = intro;