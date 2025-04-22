// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Auth {
    mapping(bytes32 => string) private hashes;

    function storeHash(string memory userHash, string memory mediaHash) public {
        hashes[keccak256(abi.encodePacked(userHash))] = mediaHash;
    }

    function getHash(string memory userHash) public view returns (string memory) {
        return hashes[keccak256(abi.encodePacked(userHash))];
    }
}
    