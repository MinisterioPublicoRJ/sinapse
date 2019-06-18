import {
    formatCNPJ,
    formatCPF,
    formatCPFOrCNPJ,
    formatDate,
    formatDocumentHierarchy,
    formatMPRJ,
    formatVehiclePlate,
    getNodeType,
    typeNameSingular,
    typeNamePlural,
} from '/static/js/utils.js'

import { addOnClickListenerDelete, addOnClickListenerHide } from './main.js'

const sidebarLeft = document.getElementById("entitylist")

/**
 *
 * @param {Object[]} nodes Array of nodes to be sorted
 * @param {String} type The type of node (which varies the key to sort them)
 */
const sortByType = (nodes, type) => {
    switch (type) {
        case 'documento':
            return sortByProperty(nodes, 'nr_mp')
        case 'empresa':
            return sortByProperty(nodes, 'razao_social')
        case 'multa':
            return sortByProperty(nodes, 'data')
        case 'orgao':
            return sortByProperty(nodes, 'nm_orgao')
        case 'personagem':
            return sortByProperty(nodes, 'pers_nm_pessoa')
        case 'pessoa':
                return sortByProperty(nodes, 'nome')
        default:
            return nodes
    }
}

/**
 * Sorts a node Array
 * @param {Object[]} nodes Array of nodes to be sorted
 * @param {Object} nodes[].properties
 * @param {Object} nodes[].properties.prop A number of string to be sorted.
 * @param {String} prop The name of the property to sort.
 */
const sortByProperty = (nodes, prop) => nodes.sort((a, b) => (a.properties[prop] > b.properties[prop]) ? 1 : -1)

/**
 * Returns a DOM string for a node on the sidebar
 * @param {Object} node
 * @param {Object} node.properties
 * @param {String[]} node.type
 */
const nodeToDOMString = node => {
    let ret = `<dt>`
    if (node) {
        const type = node.type[0].toLowerCase();
        const eye = `<a class="${type} entity-item fa fa-eye icon" role="button" data-node="${node.id}"></a>`
        const trashcan = `<a class="${type} fa fa-trash icon" onclick="deleteSingleNode(${node.id})"></a>`
        const icons = `<span class="expand-span">${eye}${trashcan}</span>`
        switch (getNodeType(node)) {
            case 'documento':
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${formatMPRJ(node.properties.nr_mp)}</a>${icons}<dd>${formatDate(node.properties.dt_cadastro)} - ${formatDocumentHierarchy(node.properties.cldc_ds_hierarquia)}</dd>`
                break
            case 'embarcacao':
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${node.properties.nome_embarcacao}</a>${icons}`
                break
            case 'empresa':
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${node.properties.nome_fantasia || node.properties.razao_social}</a>${icons}<dd>CNPJ: ${formatCNPJ(node.properties.num_cnpj)}</dd>`
                break
            case 'multa':
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${formatDate(node.properties.datainfra)} - ${node.properties.descinfra}</a>${icons}`
                break
            case 'orgao':
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${node.properties.nm_orgao}</a>${icons}`
                break
            case 'pessoa':
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${node.properties.nome}</a>${icons}`
                if (node.properties.cpf) {
                    ret += `<dd>CPF: ${formatCPF(node.properties.num_cpf)}</dd>`
                }
                break
            case 'personagem':
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${node.properties.pess_nm_pessoa} - ${node.properties.tppe_descricao}</a>${icons}<dd>CPF/CNPJ: ${formatCPFOrCNPJ(node.properties.cpfcnpj)}</dd>`
                break
            case 'veiculo':
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${node.properties.marca_modelo.trim()} ${node.properties.fabric}/${node.properties.modelo} ${node.properties.descricao_cor.trim()} - ${formatVehiclePlate(node.properties.placa)}</a>${icons}`
                break
            default:
                ret += `<a class="item-line" onclick="zoomToNodeId(${node.id})">${node.id}</a>${icons}`
        }
        ret += `</dt>`
    }

    return ret
}

/**
 * Updates left sidebar with entities to zoom
 * @param {String[]} labels Labels list
 * @param {Object[]} nodesData Nodes properties list
 */
export const updateLeftSidebar = (labels, nodesData) => {
    document.querySelector('.entitylist').style.display = 'block'
    let entityListToWrite = ''

    $(() => $(".entitylist").dialog({
        classes: {
            "ui-dialog-titlebar-close": "graphhidden",
            "ui-dialog": "not-printable",
        },
        height: 500,
        position: {
            my: 'left',
            at: 'left',
        },
        title: 'lista de vínculos'
    }))

    labels.sort().forEach(type => {
        type = type.toLowerCase()
        let nodesForThisType = sortByType(nodesData.filter(node => getNodeType(node) === type), type)
        if (nodesForThisType.length) {
            entityListToWrite += `
                <h2>
                    <a data-toggle='collapse' href='#collapse-${type}' role='button' class='color-${type} collapsed'>> ${nodesForThisType.length > 1 ? typeNamePlural(type) : typeNameSingular(type)}</a>
                    <span class="expand-span">
                      <a class="color-${type} ${type} entity fa fa-eye icon" role="button"></a>
                      <a class="color-${type} ${type} entity-trash fa fa-trash icon" role="button"></a>
                    </span>
                </h2>
                <dl class='collapse' id='collapse-${type}'>
            `
            nodesForThisType.forEach(node => {
                entityListToWrite += nodeToDOMString(node)
            })
            entityListToWrite += `</dl>`
        }
    })

    sidebarLeft.innerHTML = entityListToWrite
    addOnClickListenerDelete();
    addOnClickListenerHide();
}

export const filterEntityList = () => {
    let filteredValue = document.querySelector('#entitylistfilter').value
    // expand all categories
    document.querySelectorAll('.collapsed').forEach(e => e.click())
    // show matched items, hide otherwise
    document.querySelectorAll('#entitylist dt').forEach(e => {
        if (e.innerText.toLowerCase().includes(filteredValue.toLowerCase())) {
            $(e).show()
            $(e.nextElementSibling).show()
        } else {
            $(e).hide()
            $(e.nextElementSibling).hide()
        }
    })
}
