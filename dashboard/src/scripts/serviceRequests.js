const axios = require('axios');
const url = 'http://localhost'
const event1 = ':8200/get_event_1_seq'
const event2 = ':8200/get_latest_request_form?Content-Type=application/json'
const eventStats = ':8100/events/stats?Content-Type=application/json'

export const get_event_1_seq = async(seqNum) => {
    const data = await axios.get(url + event1 + '?seqNum=' + seqNum).then((result) =>{
                return result.data
            }).catch(e=>{console.log('get_event_1_seq error.')})
    return data
}

export const get_latest_request_form = async() => {
    const data = await axios.get(url + event2).then(result => {
                        return result.data
                        }).catch(e => {console.log('get_latest_request_form error.')})
    return data
}

export const get_form_stats = async() => {
    const data = await axios.get(url + eventStats).then(result => {
                        return result.data
                        }).catch(e => {console.log('get_form_stats.')})
    return Promise.resolve(data)
}
