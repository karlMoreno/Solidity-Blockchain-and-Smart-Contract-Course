// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage { //inheritance; StorageFactory has all the functions of SimpleStorage

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorage() public {
        SimpleStorage simpleStorage = new SimpleStorage(); // variable simpleStorage has type of SimpleStorage which becomes a new contract that takes no parameters
        simpleStorageArray.push(simpleStorage);
    }


    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
    //needs Adress
    //needs ABI Application Binary Interface
    
    SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).store(_simpleStorageNumber);

    //^^^^^
    //SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
    //simpleStorage.store(_simpleStorageNumber);
    }

    function sfGet(uint256 _simpleStorageIndex) public view returns (uint256) {
        return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve();
        
        //SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        //return simpleStorage.retrieve(); is this^^^
    }
}
