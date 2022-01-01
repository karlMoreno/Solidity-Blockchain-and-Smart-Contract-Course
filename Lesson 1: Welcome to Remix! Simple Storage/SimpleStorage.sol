// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // unassigned variables are given null or 0
    uint256 public favoriteNumber;
    //structs are used to create records
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    // mappings are a dictionayr like data structure, with 1 value per key
    mapping(string => uint256) public nameToFavoriteNumber;


    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    //view, pure dont need to make a transaction
    //view reads off the chain so dont state change
    // pure purely does math 
    function retrieve() public view returns(uint256)  {
        return favoriteNumber;
    }
    //memory:data will only be stored during the execution of the function
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

}
