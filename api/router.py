from fastapi import APIRouter, HTTPException, status
from shemas.shemas import Example, RoleAssignment

from web3.middleware import geth_poa_middleware

from web3 import Web3

# Step 2: Connect to your local Ethereum node
web3 = Web3(Web3.HTTPProvider("https://validator3.rpc.bc24.miage.dev"))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_address = "0x42699A7612A82f1d9C36148af9C77354759b210b"
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


@router.post("/assign-role")
async def assign_role(data: RoleAssignment):
    # Ensure the wallet address is valid
    if not web3.is_address(data.wallet_address):
        raise HTTPException(status_code=400, detail="Invalid wallet address")

    # Replace these with your account details
    account = web3.eth.account.from_key(
        "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63")

    # Prepare the transaction
    txn_dict = contract.functions.giveUserRole(data.wallet_address, data.role).build_transaction({
        "from": account.address,
        'chainId': 1337,  # Mainnet. Change accordingly if you're using a testnet
        'nonce': web3.eth.get_transaction_count(account.address),
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(
        txn_dict, private_key=account.key)

    # Send the transaction
    txn_receipt = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_receipt)

    print(txn_receipt)

    return {"status": "success", "transaction_hash": txn_receipt.transactionHash.hex()}


@router.get("/test_mint")
async def test():
    # Account details
    # Replace YOUR_ACCOUNT_ADDRESS
    account = web3.eth.account.from_key(
        "99f55cdda1001d13735212a7cd2944f12460046f8c26c17d784ccaa0042eeb62")

    # Function parameters
    resourceId = 1  # Example resourceId
    quantity = 1  # Example quantity
    _metaData = "Example metadata"  # Example metadata
    ingredients = []  # Example ingredients

    # Build the transaction
    transaction = contract.functions.mintRessource(resourceId, quantity, _metaData, ingredients).build_transaction({
        "from": account.address,
        'chainId': 1337,
        "gasPrice": web3.eth.gas_price,
        "nonce": web3.eth.get_transaction_count(account.address),
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(
        transaction, private_key=account.key)

    # Send the transaction

    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

    print(txn_receipt.logs)

    return {"Transaction successful with hash"}


@router.get("/ResourceCreatedEvents")
async def ResourceCreatedEvents():
    # Testing the event filters
    last_event = contract.events.ResourceCreatedEvent.get_logs(fromBlock=1)[
        0].args

    return {"Event": last_event}


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
