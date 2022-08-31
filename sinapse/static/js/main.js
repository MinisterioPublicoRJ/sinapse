import {
    addStyleToNode,
    complianceNoProcedure,
    complianceProcedure,
    formatKeyString,
    formatPropString,
    formatAddresses,
    get,
    getCardTitle,
    getNodeType,
    sanitizeQuery,
    showCompliance,
    showComplianceForm,
    showLoading,
    hideLoading,
    thousandsSeparator,
    typeNameSingular,
    typeNamePlural,
} from '/static/js/utils.js'
import { entityCard } from '/static/js/cards.js'
import { updateLeftSidebar, filterEntityList } from '/static/js/entitylist.js'

/**
 * Init function called on window.onload.
 */
const init = () => {
    getLabels()
    initSearch()
    initVisjs()
    initVersion()
}

const VERSION = '20190625'
let SEARCH_TAB_OPENED = 2
const EDGES_DICT = {
    'orgao_responsavel': 'órgão responsável',
    'parte_de': 'parte de',
    'proprietario': 'proprietário',
    'socio': 'sócio',
    'socio_responsavel': 'sócio responsável',
    'MAE': 'mãe',
    'PAI': 'pai',
}
let homonymAlertDisplayed = false

// Initial vars
let nodes,               // Visjs initialized nodes
    nodesData,           // Nodes array as is from API
    edges,               // Visjs initialized edges (path between nodes)
    edgesData,           // Edges array as is from API
    searchData,          // Data last returned by search API
    filteredEntityTypes, // Entity types we don't want on future API queries
    container,           // Visjs DOM element
    data,                // Object with nodes and edges
    options,             // Object that holds Visjs options
    network,             // Visjs Network, linking container, data and options
    photosData,
    labels,
    complianceData        // compliance data for the printed version

const baseIconsPath = '/static/img/icon/graph/'
const sidebarRight = document.getElementById("sidebarRight")

const initVisjs = () => {
    // initialize everything as empty (we don't have data yet)
    nodesData = []
    edgesData = []
    photosData = {}
    filteredEntityTypes = []
    nodes = new vis.DataSet([])
    edges = new vis.DataSet([])
    container = document.getElementById('graph')
    data = { nodes, edges }
    options = {
        edges: {
            color: {
                inherit: 'from',
            },
        },
        interaction:{
            hover: true,
        },
        locale: 'pt-br',
        locales: {
            'pt-br': {
                del: 'Apagar nó selecionado',
                edit: 'Editar',
            },
        },
        manipulation: {
            enabled: false,
        },
        nodes: {
            chosen: {
                node(values) {
                    values.borderWidth = 10
                    values.size = 30
                },
            },
        },
        physics: {
            solver: 'forceAtlas2Based',
            stabilization: {
                enabled: true,
                iterations: 1000,
                updateInterval: 25
            },
        },
    }
    network = new vis.Network(container, data, options)

    // Don't change to arrow function (`this` wouldn't work)
    network.on('click', function(params) {
        const selectedNodeId = this.getNodeAt(params.pointer.DOM)
        if (selectedNodeId) {
            const selectedNode = nodesData.filter(node => node.id === selectedNodeId)[0]
            console.log(selectedNode)
            populateSidebarRight(selectedNode)
            showSidebarRight()
        } else {
            emptySidebarRight()
            hideSidebarRight()
        }
    })
    network.on('doubleClick', function(params) {
        const selectedNodeId = this.getNodeAt(params.pointer.DOM)
        if (selectedNodeId) {
            getNextNodes(selectedNodeId)
        }
    })
    network.on('oncontext', function(params) {
        container.oncontextmenu = () => false // Cancels right click menu
    })
}

/**
 * Gets
 * @param {Number} nodeId A Node ID to fetch from API
 */
const getNextNodes = nodeId => {
    get(`/api/nextNodes?node_id=${nodeId}`, data => updateNodes(data, nodeId))
}

/**
 * Gets labels from the API.
 */
const getLabels = () => {
    get('/api/labels', setLabels)
}

/**
 * Sets labels and create a DOM element for each of them. Also initializes buttons events.
 *
 * @param {String[]} labels An array of labels as strings.
 */
const setLabels = data => {
    // store it
    labels = data

    // hides loading
    hideLoading()

    // displays search
    document.querySelector('#search-area').className = ''
}

/**
 * Initialize search
 */
const initSearch = () => {
    document.getElementById('form-search-area').addEventListener('submit', e => {
        e.preventDefault()
        showLoading()
        document.querySelector('#search-result').innerHTML = ''
        get(`/api/search?q=${sanitizeQuery(e.target[0].value)}`, searchCallback)
    })
}

/**
 * Updates default opened tab with the type with most documents returned
 * @param {*} data The whole data returned from API
 */
const updateOpenedTab = data => {
    let tabsArray = []
    Object.keys(data).forEach((key, index) => {
        tabsArray.push({
            id: index,
            name: key,
            quantity: data[key].response.numFound
        })
    })
    tabsArray.sort((a, b) => b.quantity - a.quantity)
    // return pessoa (if available) or empresa (if available) or the type with most quantity
    if (tabsArray.filter(t => t.name === 'pessoa')[0].quantity) {
        return tabsArray.filter(t => t.name === 'pessoa')[0].id
    }
    if (tabsArray.filter(t => t.name === 'pessoa_juridica')[0].quantity) {
        return tabsArray.filter(t => t.name === 'pessoa_juridica')[0].id
    }
    return tabsArray[0].id
}

/**
 * Creates tabs for entity search
 * @param {*} data The whole data returned from API, to get highlight information
 * @param {bool} bondSearchId whether the card is being called within the bond search list result or in the main search screen
*/
const createSearchTabs = (data, bondSearchId) => {
    SEARCH_TAB_OPENED = updateOpenedTab(data)
    let finalHTML = '<ul class="nav nav-tabs" role="tablist">'

    // first it iterates each 'object_type' (empresa, pessoa, veiculo) to create tabs
    Object.keys(data).forEach((key, index) => {
        let tabLink = bondSearchId ? `bond_${key}` : key
        finalHTML += `<li role="presentation" ${index === SEARCH_TAB_OPENED ? 'class="active"' : ''}>
            <a href="#${tabLink}" role="tab" class="custom-tab ${key}" data-toggle="tab">
                <img src="/static/img/icon/${key}.svg" />
                <p class="number color-${key}">${thousandsSeparator(data[key].response.numFound)}</p>
                <p class="color-${key}">${data[key].response.numFound > 1 ? typeNamePlural(key) : typeNameSingular(key)}</p>
            </a>
        </li>`
    })

    finalHTML += '</ul>'
    return finalHTML
}

/**
 * Creates cards with entity search results
 * @param {*} data The whole data returned from API, to get highlight information
 * @param {bool} bondSearchId whether the card is being called within the bond search list result or in the main search screen
*/
const createSearchCards = (data, bondSearchUuid, bondSearchType) => {
    let finalHTML = '<div class="tab-content">'

    // then, for each 'object_type', create a tab panel
    Object.keys(data).forEach((key, indexKey) => {
        let tabId = bondSearchUuid ? `bond_${key}` : key
        finalHTML += `<div role="tabpanel" class="tab-pane ${indexKey === SEARCH_TAB_OPENED ? 'active' : ''} ${key}" id="${tabId}">`
        // and for each 'doc', create a card
        data[key].response.docs.forEach(doc => {
            finalHTML += entityCard(doc, key, data, false, bondSearchUuid, bondSearchType)
        })
        // treat empty result
        if (data[key].response.docs.length === 0) {
            finalHTML += '<p>Não há resultados para este tipo de entidade para o valor pesquisado.'
        }
        finalHTML += '</div>'
    })
    finalHTML += '</div>'

    return finalHTML
}

/**
 * Creates entity search result
 * @param {*} data The whole data returned from API, to get highlight information
 * @param {Number} bondSearchId whether the card is being called within the bond search list result or in the main search screen
*/
const createSearchContent = (data, bondSearchUuid, bondSearchType) => createSearchTabs(data, bondSearchUuid, bondSearchType) + createSearchCards(data, bondSearchUuid, bondSearchType)

/**
 * Function called when search call is returned from API
 * @param {Object} data data from API
 * @param {Object} data.object_type objects of a given type that matches this search term. currently supported are: empresa, pessoa, veiculo
 * @param {Object} data.object_type.highlighting highlighted terms returned by search
 * @param {Object} data.object_type.highlighting.uuid a object that has a highlighted term
 * @param {String[]} data.object_type.highlighting.uuid.prop the terms that matches the searched term
 * @param {Object} data.object_type.response the data that matches the searched term
 * @param {Object[]} data.object_type.response.docs each matched object data (entity)
 * @param {Number} data.object_type.respose.numFound the quantity of items matching this search
 * @param {Number} data.object_type.response.start first item, should be 0 unless making pagination
 */
const searchCallback = data => {
    hideLoading()
    searchData = data
    document.querySelector('#balls-animation').style.display = 'none'
    document.querySelector('#search-result').innerHTML = createSearchContent(data)
}

const addVeiculoFoto = data => {
    console.log(data)
}

const backToSearch = () => {
    document.querySelector('#search-area').style.display = 'block'
    document.querySelector('#search-result').style.display = 'block'
    document.querySelector('#search-details').style.display = 'none'
}

const searchDetailStep = (entityUUID, entityType) => {
    document.querySelector('#search-area').style.display = 'none'
    document.querySelector('#search-result').style.display = 'none'
    document.querySelector('#search-details').style.display = 'block'
    let searchedDoc = searchData[entityType].response.docs.filter(doc => doc.uuid === entityUUID)[0]
    console.log(entityUUID, entityType, searchedDoc)

    let searchWhereaboutsFn = `searchWhereabouts('${entityUUID}', '${searchedDoc.nome}', '${searchedDoc.rg}')`
    if (entityType !== 'pessoa') {
        searchWhereaboutsFn = `alert('Função disponível somente para busca por pessoas físicas.')`
    }

    let searchDetailsHTML = `<div class="${entityType}">
        ${entityCard(searchedDoc, entityType, searchData, true)}
        <div class="col-lg-4 action busca-paradeiro" onclick="${searchWhereaboutsFn}">
            Busca<br>
            <b>Paradeiro</b>
        </div>
        <div class="col-lg-4 action caminho-exploratorio" onclick="showEntity('${searchedDoc.label}', '${entityUUID}')">
            Caminho<br>
            <b>Exploratório</b>
        </div>
        <div class="col-lg-4 action analise-de-vinculos" onclick="bondAnalysis('${entityUUID}','${searchedDoc.label}','${searchedDoc[getCardTitle(entityType)]}')">
            Análise de<br>
            <b>Vínculos</b>
        </div>
    </div>`

    document.querySelector('#search-details').innerHTML = searchDetailsHTML
}

/**
 * Gets from API the nodes that match the given label, prop and val.
 *
 * @param {string} label
 * @param {string} prop
 * @param {string} val
 */
const findNodes = (label, prop, val) => {
    if (!label || !prop || !val) {
        return alert('ERRO: É preciso escolher o tipo, a propriedade e preencher um valor para realizar uma busca.')
    }
    get(`/api/findNodes?label=${label}&prop=${prop}&val=${val}`, updateFromFindNodes)
}

/**
 * Call getNextNodes on node returned by findNodes, so the graph comes already expanded on first level (instead of a single node)
 * @param {Object} data
 * @param {Object[]} data.nodes
 * @param {String} data.nodes[].id
 */
const updateFromFindNodes = data => {
    if (data.nodes[0]) {
        getNextNodes(data.nodes[0].id)
    }
}

/**
 * Update nodes with given API data.
 *
 * @param {*} data Data from API data.
 */
const updateNodes = (data, nodeId) => {
    hideLoading()
    document.querySelector('.busca').style.display = 'none'
    document.querySelector('footer').className = ''
    document.querySelector('#graph').className = ''
    // update graph. notice we only add non-existant nodes/edges - no duplicates are allowed.
    if (data.nodes) {
        for (let node of data.nodes) {
            // check if this node already exists checking its id
            let filteredNode = nodesData.filter(n => n.id === node.id)
            const type = node.type[0].toLowerCase();

            if (filteredNode.length === 0 && (filteredEntityTypes.indexOf(type) === -1)) {
              //console.log('node: ', node)
                // doesn't exist, add it
                let formattedNode = addStyleToNode(node)
                nodesData.push(formattedNode)
                nodes.add(formattedNode)
            }
            // if it's a person or vehicle, check if we can add it to our photos array
            let nodeType = getNodeType(node)
            if (
                (
                    (nodeType === 'pessoa' && node.properties.num_rg) ||
                    (nodeType === 'veiculo')
                )
                && !photosData[node.uuid]
            ) {
                let imageEndpoint
                switch (nodeType) {
                    case 'pessoa':
                        imageEndpoint = `/api/foto?rg=${node.properties.num_rg}`
                        break;
                    case 'veiculo':
                        imageEndpoint = `/api/foto-veiculo?caracteristicas=${node.properties.marca_modelo} ${node.properties.modelo} ${node.properties.descricao_cor}`
                        break;
                }
                get(imageEndpoint, data => {
                    if (data.uuid && data.imagem) {
                        if (!photosData[data.uuid]) {
                            photosData[data.uuid] = data
                            let matchedNode = nodesData.filter(node => node.properties.uuid === data.uuid)
                            if (matchedNode && matchedNode[0]) {
                                nodes.update({id: matchedNode[0].id, shape: 'circularImage', image: `data:image/png;base64,${data.imagem}`})
                            }
                        }
                    }
                })
            }
        }
    }
    if (data.edges) {
        let motherCount = 0
        let fatherCount = 0
        for (let edge of data.edges) {
            // the same for edges
            let filteredEdge = edgesData.filter(e => e.id === edge.id)
            if (filteredEdge.length === 0) {
                if (edge.label) {
                    edge.label = edge.label.toLowerCase()
                    if (edge.properties.parentesco) {
                        if (edge.from == nodeId && edge.properties.parentesco === 'MAE') {
                            motherCount++
                        }
                        if (edge.from == nodeId && edge.properties.parentesco === 'PAI') {
                            fatherCount++
                        }
                        edge.label = edge.properties.parentesco
                    }
                    // fix diacritics
                    edge.label = edge.label in EDGES_DICT ? EDGES_DICT[edge.label] : edge.label
                }
                if (edge.properties.dt_fim) {
                    edge.dashes = true
                    if (edge.label === 'trabalha') {
                        edge.label = 'trabalhou'
                    }
                }
                edgesData.push(edge)
                edges.add(edge)
            }
        }
        if ( (motherCount > 1 || fatherCount > 1) && !homonymAlertDisplayed ) {
            homonymAlertDisplayed = true
            alert('ATENÇÃO: O sistema pode exibir homônimos em idade compatível para relação parental.')
        }
    }

    // show back button
    document.getElementById('step4').className = ''

    updateLeftSidebar(labels, nodesData)

    document.querySelectorAll('#entitylist .entity-item').forEach(itemLabel => {
        itemLabel.onclick = e => {
            const nodeId = itemLabel.dataset.node;
            if (itemLabel.classList.contains('fa-eye-slash')) {
                itemLabel.classList.remove('fa-eye-slash');

                const updatedNodes = [];
                updatedNodes.push({id: nodeId, hidden: false});
                nodes.update(updatedNodes);
            } else {
                itemLabel.classList.add('fa-eye-slash');

                const updatedNodes = [];
                updatedNodes.push({id: nodeId, hidden: true});
                nodes.update(updatedNodes);
            }
        }
    })
}

export const addOnClickListenerHide = () => {
  document.querySelectorAll('#entitylist .entity').forEach(filter => {
      filter.onclick = e => {
          let entityType = filter.classList[1]
          if (filter.classList.contains('fa-eye-slash')) {
              filter.classList.remove('fa-eye-slash')
              filteredEntityTypes.splice(filteredEntityTypes.indexOf(entityType), 1)
          } else {
              filter.classList.add('fa-eye-slash')
              filteredEntityTypes.push(entityType)
          }
          updateFilteredEntityTypes()
      }
  })
}

export const addOnClickListenerDelete = () => {
  document.querySelectorAll('#entitylist .entity-trash').forEach(filter => {
    filter.onclick = e => {
        // find all the nodes from that category
        const entityType = filter.classList[1];
        const nodesFromType = nodesData
        .filter(node => node.type[0].toLowerCase() === entityType)
        .map(node => node.id);

        // delete them
        network.selectNodes(nodesFromType);
        network.deleteSelected();

        // delete the label from the current list of labels and to the list of ignored labels
        labels = labels.filter(label => label.toLowerCase() !== entityType)
        filteredEntityTypes.push(entityType)
        console.log(filteredEntityTypes);
        updateLeftSidebar(labels, nodesData)
    }
  })
}

/**
 * Zooms to a given nodeId
 * @param {String} nodeId
 */
const zoomToNodeId = nodeId => {
    network.focus(nodeId, { scale: 2, animation: true })
    const selectedNode = nodesData.filter(node => node.id === nodeId.toString())[0] // nodeId comes as Number, node.id is a String
    populateSidebarRight(selectedNode)
    showSidebarRight()
    network.selectNodes([nodeId.toString()])
}

/**
 * Deletes a single node from the graph
 * @param  {[string]} id nodeId
 */
const deleteSingleNode = (id) => {
  // delete label for that node
    const filteredNodes = nodesData
    .filter(node => node.id !== id.toString());
    nodesData = filteredNodes;
    updateLeftSidebar(labels, nodesData);

  // delete
  network.selectNodes([id]);
  network.deleteSelected();
}

const emptySidebarRight = () => {
    while (sidebarRight.hasChildNodes()) {
        sidebarRight.removeChild(sidebarRight.firstChild)
    }
}

/**
 * Populates Right Sidebar with data form a node.
 *
 * @param {Object} node A node from Neo4J.
 */
const populateSidebarRight = node => {
    sidebarRight.setAttribute('class', getNodeType(node))

    emptySidebarRight()

    let html = `<div id="content">
        <div class="header bgcolor-${getNodeType(node)}">`
    // Add person photo
    let nodeType = getNodeType(node)
    if (
        (
            (nodeType === 'pessoa' && node.properties.num_rg) ||
            (nodeType === 'veiculo')
        )
        && photosData[node.properties.uuid]
    ) {
        let imageLink = `data:image/png;base64,${photosData[node.properties.uuid].imagem}`
        html += `<img src="${imageLink}">`
    }
    html += `</div>
    <div id="valuesContainer">`
    Object.keys(node.properties).forEach(property => {
        if (
            property === 'filho_rel_status' ||
            property === 'filho_rel_status_pai' ||
            property === 'uuid' ||
            property === 'sensivel' ||
            property.substr(0,1) === '_' ||
            property.substr(-3) === '_dk' ||
            property.substr(0,3) === 'cd_'
        ) {
            return // skip this property
        }

        html += `<span class="sidebarRight-label">${formatPropString(property)}</span>
        <span class="sidebarRight-data color-${nodeType}">${formatKeyString(property, node.properties[property])}</span>`
    });
    html += `</div>
        <button id="fullSidebarRight" onclick="fullSidebarRight()"></button>
    </div>`

    sidebarRight.innerHTML = html
}

/**
 * Displays the Right Sidebar.
 */
const showSidebarRight = () => {
    sidebarRight.style.display = "block"
    document.getElementsByTagName('body')[0].className = 'showingSidebarRight'
    $(() => $("#sidebarRight").dialog({
        classes: {
            "ui-dialog-titlebar": `bgcolor-${$("#sidebarRight")[0].className}`,
        },
        height: 600,
        position: {
            my: "right",
            at: "right",
        },
    }))
}

/** Hides the Right Sidebar. */
const hideSidebarRight = () => {
    document.getElementById('sidebarRight').style.display = "none"
    sidebarRight.style.display = "none"
    document.getElementsByTagName('body')[0].className = ''
    $('#sidebarRight').dialog('close')
}

/** Full/Hide the Right Sidebar. */
const fullSidebarRight = () => {
    var x = document.getElementById("sidebarRight");
    if (x.style.width === "") {
        x.style.width = "100%";
    } else if (x.style.width === "0%") {
        x.style.width = "100%";
    } else {
        x.style.width = "0%";
    }
}

/**
 * Updates entities hidden status based on their types
 */
const updateFilteredEntityTypes = () => {
    // first make all hidden nodes visible
    let filteredNodes = []
    nodesData.filter(node => node.hidden).forEach(node => {
        filteredNodes.push({id: node.id, hidden: false})
        node.hidden = false
    })
    nodes.update(filteredNodes)

    // then hide nodes with filtered types
    filteredNodes = []
    filteredEntityTypes.forEach(type => {
        nodesData.filter(node => getNodeType(node) === type).forEach(node => {
            filteredNodes.push({id: node.id, hidden: true})
            node.hidden = true
        })
    })
    nodes.update(filteredNodes)
}

/**
 * Shows build information
 */
const initVersion = () => {
    let version = `${VERSION}-${btoa(document.getElementById('version_username').innerHTML)}`
    document.getElementById('version_number').innerHTML = `Versão: ${version}`
    document.title = `Conexão - Versão ${version}`
}

const makeLogoGoBackToSearch = () => {
    // remove logo href link
    document.querySelector('#conexaologo').removeAttribute('href')
    // add a click function to
    document.querySelector('#conexaologo').onclick = () => {
        // show search again
        document.querySelector('.busca').style.display = 'block'
        // hide graph
        document.querySelector('#graph').className = 'graphhidden'
        // hide sidebars
        if ($('#sidebarRight').hasClass('ui-dialog-content') && $('#sidebarRight').dialog('isOpen')) {
            // we have to test if it has been initialized first, so it doesn't error when trying to close
            $('#sidebarRight').dialog('close')
        }
        $('.entitylist').dialog('close')
    }
}

const showEntity = (entityType, uuid) => {
    console.log(`showEntity(${entityType}, ${uuid})`)
    makeLogoGoBackToSearch()
    document.querySelector('.busca').style.display = 'none'
    findNodes(entityType, 'uuid', uuid)
}

const bondAnalysis = (nodeUuid1, nodeType1, nodeTitle1) => {
    document.querySelector('#search-details').style.display = 'none'
    console.log(`bondAnalysis(${nodeUuid1}, ${nodeType1}, ${nodeTitle1})`)
    let template = `
    <div class="row">
        <div class="col-lg-5 color-${nodeType1.toLowerCase()} entity">
            <img src="/static/img/icon/${nodeType1}.svg"/>
            <input class="color-${nodeType1}" disabled value="${nodeTitle1}">
        </div>
        <div class="col-lg-2">
            <div class="add-bond">
                <img src="/static/img/icon/icon-vinculos.svg" />
            </div>
            <p class="text">
                Análise de <br />
                <b>Vínculos</b>
            </p>
        </div>
        <div id="bond-search" class="col-lg-5 entity entity-empty">
            <img src="/static/img/icon/vinculo-empty.svg"/>
            <form id="form-bond-search">
                <input class="color-veiculo" value="" placeholder="Procure um vínculo">
            </ form>
        </div>
    </div>
    <div class="row">
        <div class="col-lg-5"></div>
        <div class="col-lg-7">
            <div id="bond-search-result"></div>
        </div>
    </div>
    `
    document.querySelector('#bond-analysis').innerHTML = template
    document.getElementById('form-bond-search').addEventListener('submit', e => {
        e.preventDefault()
        showLoading()
        document.querySelector('#bond-search-result').innerHTML = ''
        get(`/api/search?q=${sanitizeQuery(e.target[0].value)}`, data => {
            bondSearchCallback(data, nodeUuid1, nodeType1)
        })
    })
}

const bondSearchCallback = (data, nodeUuid1, nodeType1) => {
    hideLoading()
    document.querySelector('#bond-search-result').innerHTML = createSearchContent(data, nodeUuid1, nodeType1)
}

const doBondSearch = (nodeUuid1, nodeType1, nodeUuid2, nodeType2) => {
    showLoading()
    getShortestPath(nodeUuid1, nodeType1, nodeUuid2, nodeType2)
}

const getShortestPath = (nodeUuid1, nodeType1, nodeUuid2, nodeType2) => {
    get(`/api/findShortestPath?node_uuid1=${nodeUuid1}&label1=${nodeType1}&node_uuid2=${nodeUuid2}&label2=${nodeType2}`, updateNodes)
    makeLogoGoBackToSearch()
}

/**
 * Searches for a person whereabouts
 * @param {String} nodeUuid
 * @param {String} nome
 * @param {String} rg
 */
const searchWhereabouts = (nodeUuid, nome, rg) => {
    document.querySelector('#search-details').style.display = 'none'

    get(`/api/whereaboutsReceita?uuid=${nodeUuid}`, dataReceita => {
        displayWhereabouts(dataReceita, nome, rg)
        get(`/api/whereaboutsCredilink?uuid=${nodeUuid}`, dataCredilink => { displayCredilinkWhereabouts(dataCredilink) })
    })

    showLoading()
}

/**
 * Displays information about a person whereabouts
 * @param {Object[]} data
 * @param {Object[]} data[].formatted_addresses
 * @param {String} data[].formatted_addresses[].bairro
 * @param {String} data[].formatted_addresses[].cep
 * @param {String} data[].formatted_addresses[].cidade
 * @param {String} data[].formatted_addresses[].complemento
 * @param {String} data[].formatted_addresses[].endereco
 * @param {String} data[].formatted_addresses[].numero
 * @param {String} data[].formatted_addresses[].sigla_uf
 * @param {String} data[].formatted_addresses[].telefone
 * @param {String} data[].type
 * @param {String} nome
 * @param {String} rg
 */
const displayWhereabouts = (dataReceita, nome, rg) => {
    hideLoading()

    document.querySelector('#whereabouts').innerHTML = `
        <div class="row pessoa">
            <div class="col-md-12">
                <h2>Busca de Paradeiros</h2>
                <h3>${nome}</h3>
            </div>
            <div class="col-md-2 text-center">
                <div id="whereabouts_photo_container"></div>
                <button onclick="hideWhereabouts()" class="back">⬅️ Voltar</button>
            </div>
            <div class="col-md-5">
                <h3>Previnity</h3>
                <p>Atenção: Informações da base de dados do Previnity não podem ser incluídos nos autos.</p>
                <div id="credilink">Carregando endereços Previnity...</div>
            </div>
            <div class="col-md-5">
                <h3>Receita Federal</h3>
                ${formatAddresses(dataReceita.formatted_addresses)}
            </div>
        </div>
    `

    get(`/api/foto?rg=${rg}`, data => {
        if (data.uuid && data.imagem) {
            document.querySelector('#whereabouts_photo_container').innerHTML = `<img class="whereabouts_photo" src="data:image/png;base64,${data.imagem}">`
        }
    })
}

const displayCredilinkWhereabouts = dataCredilink => {
    document.querySelector('#credilink').innerHTML = formatAddresses(dataCredilink.formatted_addresses)
}

const hideWhereabouts = () => {
    document.querySelector('#search-details').style.display = 'block'
    document.querySelector('#whereabouts').innerHTML = ''
}

const logout = () => {
    get('/logout', () => { location.reload() }, true)
}

const prepareToPrint = (event) => {
    // gathering procedure data
    let procNum = null
    let procObj = null
    try {
        procNum = sessionStorage.getItem('procNum')
        procObj = sessionStorage.getItem('procObj')
    } catch (e) {
        console.log('problems!')
    }

    let currentGraphData = document.querySelector('canvas').toDataURL()

    // inserting graph and footer in the print preview
    document.querySelector('#graph-data').innerHTML = `<img src="${currentGraphData}" />`;
    if (procNum) {
        document.getElementById('footnotes').innerHTML = `<p>Consulta para o processo ${procNum}, sob a justificativa '${procObj}'</p>`
    }
}

// Attach external functions to window
window.addVeiculoFoto = addVeiculoFoto
window.backToSearch = backToSearch
window.bondAnalysis = bondAnalysis
window.complianceNoProcedure = complianceNoProcedure
window.complianceProcedure = complianceProcedure
window.doBondSearch = doBondSearch
window.filterEntityList = filterEntityList
window.findNodes = findNodes
window.fullSidebarRight = fullSidebarRight
window.hideSidebarRight = hideSidebarRight
window.hideWhereabouts = hideWhereabouts
window.logout = logout
window.searchDetailStep = searchDetailStep
window.searchWhereabouts = searchWhereabouts
window.showCompliance = showCompliance
window.showComplianceForm = showComplianceForm
window.showEntity = showEntity
window.zoomToNodeId = zoomToNodeId
window.deleteSingleNode = deleteSingleNode
window.prepareToPrint = prepareToPrint;
window.addEventListener('beforeprint', (event) => prepareToPrint(event));

// Finally, declare init function to run when the page loads.
window.onload = init
