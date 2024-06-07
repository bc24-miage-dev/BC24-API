from fastapi import APIRouter, HTTPException, status
from shemas.shemas import Example

from web3 import Web3

# Step 2: Connect to your local Ethereum node
web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "admin",
                "type": "address"
            },
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "ressource_id",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "ressource_name",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "needed_resources",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "needed_resources_amounts",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "initial_amount_minted",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "required_role",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "produces_resources",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "produces_resources_amounts",
                        "type": "uint256[]"
                    }
                ],
                "internalType": "struct BC24_Update.ResourceTemplate[]",
                "name": "_ressourceTemplates",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "AccessControlBadConfirmation",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "bytes32",
                "name": "neededRole",
                "type": "bytes32"
            }
        ],
        "name": "AccessControlUnauthorizedAccount",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "balance",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "needed",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "ERC1155InsufficientBalance",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "approver",
                "type": "address"
            }
        ],
        "name": "ERC1155InvalidApprover",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "idsLength",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "valuesLength",
                "type": "uint256"
            }
        ],
        "name": "ERC1155InvalidArrayLength",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "operator",
                "type": "address"
            }
        ],
        "name": "ERC1155InvalidOperator",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "receiver",
                "type": "address"
            }
        ],
        "name": "ERC1155InvalidReceiver",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "name": "ERC1155InvalidSender",
        "type": "error"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "operator",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "ERC1155MissingApprovalForAll",
        "type": "error"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "operator",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "ApprovalForAll",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "ressourceName",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "message",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "ResourceCreatedEvent",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "string",
                                "name": "required_role",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "dataString",
                                "type": "string"
                            },
                            {
                                "internalType": "address",
                                "name": "lastModifiedBy",
                                "type": "address"
                            },
                            {
                                "internalType": "uint256",
                                "name": "lastModifiedAt",
                                "type": "uint256"
                            }
                        ],
                        "internalType": "struct BC24_Update.Data[]",
                        "name": "data",
                        "type": "tuple[]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "resourceId",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "ressourceName",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "ingredients",
                        "type": "uint256[]"
                    }
                ],
                "indexed": False,
                "internalType": "struct BC24_Update.MetaData",
                "name": "metaData",
                "type": "tuple"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "ResourceMetaDataChangedEvent",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "previousAdminRole",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "newAdminRole",
                "type": "bytes32"
            }
        ],
        "name": "RoleAdminChanged",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "name": "RoleGranted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"
            }
        ],
        "name": "RoleRevoked",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "operator",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "ids",
                "type": "uint256[]"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "values",
                "type": "uint256[]"
            }
        ],
        "name": "TransferBatch",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "operator",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "TransferSingle",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "value",
                "type": "string"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            }
        ],
        "name": "URI",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "ADMIN_ROLE",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "DEFAULT_ADMIN_ROLE",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "ressource_id",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "ressource_name",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "needed_resources",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "needed_resources_amounts",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "initial_amount_minted",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "required_role",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "produces_resources",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "produces_resources_amounts",
                        "type": "uint256[]"
                    }
                ],
                "internalType": "struct BC24_Update.ResourceTemplate",
                "name": "template",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "quantity",
                "type": "uint256"
            },
            {
                "internalType": "uint256[]",
                "name": "ingredients",
                "type": "uint256[]"
            }
        ],
        "name": "_burnResources",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address[]",
                "name": "accounts",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "ids",
                "type": "uint256[]"
            }
        ],
        "name": "balanceOfBatch",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "uint256[]",
                "name": "ids",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256[]",
                "name": "values",
                "type": "uint256[]"
            }
        ],
        "name": "burnBatch",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            }
        ],
        "name": "getMetaData",
        "outputs": [
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "string",
                                "name": "required_role",
                                "type": "string"
                            },
                            {
                                "internalType": "string",
                                "name": "dataString",
                                "type": "string"
                            },
                            {
                                "internalType": "address",
                                "name": "lastModifiedBy",
                                "type": "address"
                            },
                            {
                                "internalType": "uint256",
                                "name": "lastModifiedAt",
                                "type": "uint256"
                            }
                        ],
                        "internalType": "struct BC24_Update.Data[]",
                        "name": "data",
                        "type": "tuple[]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "resourceId",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "ressourceName",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "ingredients",
                        "type": "uint256[]"
                    }
                ],
                "internalType": "struct BC24_Update.MetaData",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            }
        ],
        "name": "getRoleAdmin",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "role",
                "type": "string"
            }
        ],
        "name": "giveUserRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "grantRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "ressource_id",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "ressource_name",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "needed_resources",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "needed_resources_amounts",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "initial_amount_minted",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "required_role",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "produces_resources",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "produces_resources_amounts",
                        "type": "uint256[]"
                    }
                ],
                "internalType": "struct BC24_Update.ResourceTemplate",
                "name": "template",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "quantity",
                "type": "uint256"
            },
            {
                "internalType": "uint256[]",
                "name": "ingredients",
                "type": "uint256[]"
            }
        ],
        "name": "hasResourcesToMintItem",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "hasRole",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "operator",
                "type": "address"
            }
        ],
        "name": "isApprovedForAll",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "metaData",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "resourceId",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "ressourceName",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "producerToken",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_metaData",
                "type": "string"
            }
        ],
        "name": "mintOneToMany",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "resourceId",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "quantity",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_metaData",
                "type": "string"
            },
            {
                "internalType": "uint256[]",
                "name": "ingredients",
                "type": "uint256[]"
            }
        ],
        "name": "mintRessource",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "callerConfirmation",
                "type": "address"
            }
        ],
        "name": "renounceRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "ressourceTemplates",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "ressource_id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "ressource_name",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "initial_amount_minted",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "required_role",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "role",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "revokeRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256[]",
                "name": "ids",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256[]",
                "name": "values",
                "type": "uint256[]"
            },
            {
                "internalType": "bytes",
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "safeBatchTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "operator",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_metaData",
                "type": "string"
            }
        ],
        "name": "setMetaData",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "interfaceId",
                "type": "bytes4"
            }
        ],
        "name": "supportsInterface",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "tokensByResourceType",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenID",
                "type": "uint256"
            }
        ],
        "name": "uri",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "userRoles",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


contract = web3.eth.contract(address=contract_address, abi=contract_abi)


router = APIRouter()


# Only an example
fake_db = [
    {"name": "Foo Fighters", "song": "My Hero"},
    {"name": "Metallica", "song": "Hero of the Day"}
]


@router.get(
    "/examples",
    response_model=list[Example],
    status_code=status.HTTP_200_OK,
)
async def get_examples() -> list[Example]:
    return [Example(**ex)for ex in fake_db]


@router.get("/test_mint")
async def test():
    # Account details
    account_address = '0x70997970C51812dc3A010C7d01b50e0d17dc79C8'  # Replace YOUR_ACCOUNT_ADDRESS
    private_key = '0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d'  # Replace YOUR_PRIVATE_KEY

    # Function parameters
    resourceId = 1  # Example resourceId
    quantity = 1  # Example quantity
    _metaData = "Example metadata"  # Example metadata
    ingredients = []  # Example ingredients

    # Build the transaction
    transaction = contract.functions.mintRessource(resourceId, quantity, _metaData, ingredients).build_transaction({
        'chainId': 1337,
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(
        transaction, private_key=private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

    print(txn_receipt)


    return {"Transaction successful with hash": txn_hash.hex()}


@router.get("/ResourceCreatedEvents")
async def ResourceCreatedEvents():
    # Testing the event filters 
    event_filter =  contract.events.ResourceCreatedEvent.create_filter(fromBlock='latest')
    print(contract.events.ResourceCreatedEvent.get_logs(fromBlock=1))
    



   
@router.get("/status/200")
async def status_200():
    return {"status": "OK"}


@router.get("/status/403")
async def status_403():
    raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/status/404")
async def status_404():
    raise HTTPException(status_code=404, detail="Not Found")


@router.get("/status/500")
async def status_500():
    raise HTTPException(status_code=500, detail="Internal Server Error")
