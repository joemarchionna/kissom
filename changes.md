# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.11.2] - 2022 08 09
### Changed
- Changed structure of storeConfig data to include keys "isTable" and "columns"

## [1.11.1] - 2022 07 24
### Added
- isPrimaryKey parameter to createColumnDict method
### Changed
- Changed exception name
- Changed method getTableDefinition to getDefinition in storeAdapter

## [1.11.0] - 2022 07 23
### Added
- createColumnDict method

## [1.10.0] - 2022 03 01
### Fixed
- commit and rollback method issues

## [1.9.1] - 2022 02 18
### Added
- commit and rollback methods

## [1.8.0] - 2022 02 17
### Added
- condition structure methods

## [1.7.0] - 2022 02 17
### Added
- closeConnection method

## [1.6.1] - 2022 02 17
### Added
- added replace method to the manager and adapter and supporting sql and test cases
- added getObjectKeys method to the manager
### Changed
- updated setup.py to include the git-based projects using requirements files

## [1.5.0] - 2022 01 18
### Changed
- update sql building process
- broke out sql tests into specialized test classes

## [1.4.1] - 2022 01 14
### Fixed
- bug with insert in StoreManager

## [1.4.0] - 2022 01 14
### Added
- nextSequenceValue method to the StoreManager

## [1.3.1] - 2022 01 14
### Added
- xaction parameter to next method

## [1.3.0] - 2022 01 14
### Added
- sequenceName parameter to insert method

## [1.2.0] - 2022 01 14
### Added
- optional object attribute validations

## [1.1.0] - 2022 01 05
### Added
- enter and exit methods in StoreManager

## [1.0.4] - 2022 01 05
### Added
- References to kissom.__init__.py

## [1.0.0] - 2022 01 04
### Added
- Initial Release
