var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var issueSchema = new Schema({
    mentions: {
        type: Number,
        required: true,
    },
    frequency: {
        type: Number,
        required: true
    },
    word: {
        type: String,
        required: true
    },
    compound: {
        type: Number,
        required: true,
    },
    negative: {
        type: Number,
        required: true
    },
    neutral: {
        type: Number,
        required: true
    },
    positive:{
        type: String
    }
}, {
    timestamps: false
});


var issues = mongoose.model('issues', issueSchema);

module.exports = issues;