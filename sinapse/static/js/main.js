const init = () => {
    initNeo4JD3()
    getLabels()
    //initSearch()
}

const initNeo4JD3 = () => {
    var neo4jd3 = new Neo4jd3('#neo4jd3', {
        highlight: [
            {
                class: 'Project',
                property: 'name',
                value: 'neo4jd3'
            }, {
                class: 'User',
                property: 'userId',
                value: 'eisman'
            }
        ],
        icons: {
            'Api': 'gear',
            'Cookie': 'paw',
            'Email': 'at',
            'Git': 'git',
            'Github': 'github',
            'Google': 'google',
            'Ip': 'map-marker',
            'Issues': 'exclamation-circle',
            'Language': 'language',
            'Options': 'sliders',
            'Password': 'lock',
            'Phone': 'phone',
            'Project': 'folder-open',
            'SecurityChallengeAnswer': 'commenting',
            'pessoa': 'user',
            'personagem':'users',
            'veiculo': 'car',
            'empresa': 'building',
            'mgp':'balance-scale',
            'zoomFit': 'arrows-alt',
            'zoomIn': 'search-plus',
            'zoomOut': 'search-minus'
        }, 
        images: {
            'Address': 'img/twemoji/1f3e0.svg',
            'BirthDate': 'img/twemoji/1f382.svg',
            'Cookie': 'img/twemoji/1f36a.svg',
            'CreditCard': 'img/twemoji/1f4b3.svg',
            'Device': 'img/twemoji/1f4bb.svg',
            'Email': 'img/twemoji/2709.svg',
            'Git': 'img/twemoji/1f5c3.svg',
            'Github': 'img/twemoji/1f5c4.svg',
            'icons': 'img/twemoji/1f38f.svg',
            'Ip': 'img/twemoji/1f4cd.svg',
            'Issues': 'img/twemoji/1f4a9.svg',
            'Language': 'img/twemoji/1f1f1-1f1f7.svg',
            'Options': 'img/twemoji/2699.svg',
            'Password': 'img/twemoji/1f511.svg',
            'Project': 'img/twemoji/2198.svg',
            'Project|name|neo4jd3': 'img/twemoji/2196.svg',
            'User': 'img/twemoji/1f600.svg'
        },
        minCollision: 60,
        neo4jDataUrl: '/static/json/neo4jData.json',
        nodeRadius: 25,
        onNodeDoubleClick: function(node) {
            get('api/nextNodes?node_id=' + node.id, (data) => {
                neo4jd3.updateWithNeo4jData(data)
            });                        
        },
        onRelationshipDoubleClick: function(relationship) {
            console.log('double click on relationship: ' + JSON.stringify(relationship))
        },
    })
}

const getLabels = () => {
    get('/api/labels', setLabels)
}

const setLabels = labels => {
    let selectLabel = document.getElementById('selectLabel')
    selectLabel.onchange = updateProps
    labels.sort().map(label => appendOption(selectLabel, label))
}

const appendOption = (select, optionValue) => {
    var option = document.createElement('option')
    option.value = optionValue
    option.innerHTML = optionText(optionValue)
    select.appendChild(option)
}

const updateProps = () => {
    let label = document.getElementById('selectLabel').value
    getNodeProperties(label)
}

const getNodeProperties = label => {
    get(`api/nodeProperties?label=${label}`, setProps)
}

const setProps = nodeProperties => {
    let props = nodeProperties.data[0][0]
    console.log('props', props)
    let selectProp = document.getElementById('selectProp')
    props.sort().map(prop => appendOption(selectProp, prop))
}

// const initSearch = () => {
//     let tipoBusca = document.getElementById('selectBusca').value
//     let valorBusca = document.getElementById('textBusca').value
//     if (!tipoBusca || !valorBusca) {
//         return alert('É preciso escolher o tipo e preencher o valor da busca')
//     }
// }

// const getBusca

const optionText = text => {
    switch (text) {
        case 'veiculo':
            return 'Veículo'
        case 'orgao':
            return 'Órgão'
        case 'mgp':
            return 'MGP'
        default:
            return text.substr(0, 1).toUpperCase() + text.substr(1)
    }
}

const get = (url, callback) => {
    var xmlhttp = new XMLHttpRequest()
    xmlhttp.open('GET', url, true)
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4) {
            if(xmlhttp.status == 200) {
                var obj = JSON.parse(xmlhttp.responseText)
                console.log(obj)
                if (callback) {
                    callback(obj)
                }
            }
        }
    }
    xmlhttp.send(null)
}

window.onload = init
