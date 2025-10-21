var app = angular.module("mdmApp", []);

app.controller("DeviceController", function($scope, $http) {
    $scope.devices = [];
    $scope.newDevice = {};
    $scope.command = {};
    $scope.selectedDevice = null;

    // Load all devices
    $scope.loadDevices = function() {
        $http.get("/api/devices/").then(function(response){
            $scope.devices = response.data;
        });
    };

    // Add a new device
    $scope.addDevice = function() {
        if (!$scope.newDevice.device_id) {
            alert("Device ID required");
            return;
        }
        $http.post("/api/devices/add/", $scope.newDevice).then(function(response){
            alert("Device added");
            $scope.newDevice = {};
            $scope.loadDevices();
        }, function(error){
            alert(error.data.error);
        });
    };

    // Create a command for selected device
    $scope.sendCommand = function() {
        if (!$scope.selectedDevice || !$scope.command.text) {
            alert("Select device and enter command");
            return;
        }
        $http.post("/api/create_command/", {
            device_id: $scope.selectedDevice.device_id,
            command: $scope.command.text
        }).then(function(response){
            alert("Command queued: " + response.data.command_id);
            $scope.command.text = "";
        }, function(error){
            alert(error.data.error);
        });
    };

    $scope.loadDevices();
});
