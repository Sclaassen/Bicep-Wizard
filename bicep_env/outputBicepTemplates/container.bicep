// Parameters
param location string = resourceGroup().location
param containerAppName string
param environmentName string
param containerImage string
param cpuCores int = 1
param memoryGb int = 1
param subnetId string
param logAnalyticsWorkspaceId string

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' existing = {
  name: resourceGroup().name
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-06-01' existing = {
  name: logAnalyticsWorkspaceId
}

// Container App Environment
resource containerAppEnv 'Microsoft.App/managedEnvironments@2022-03-01' = {
  name: environmentName
  location: location
  properties: {
    appLogsConfiguration: {
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.properties.sharedKeys.primarySharedKey
      }
    }
    vnetConfiguration: {
      infrastructureSubnetId: subnetId
    }
  }
}

// Container App
resource containerApp 'Microsoft.App/containerApps@2022-03-01' = {
  name: containerAppName
  location: location
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 80
        transport: 'auto'
      }
      secrets: [
        {
          name: 'mySecret'
          value: 'mySecretValue'
        }
      ]
    }
    template: {
      containers: [
        {
          name: containerAppName
          image: containerImage
          resources: {
            cpu: {
              value: cpuCores
            }
            memory: {
              value: '${memoryGb}Gi'
            }
          }
        }
      ]
    }
  }
}

// Private Endpoint for Container App Environment
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  name: '${containerAppEnv.name}-pe'
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${containerAppEnv.name}-pls'
        properties: {
          privateLinkServiceId: containerAppEnv.id
          groupIds: [
            'managedEnvironment'
          ]
        }
      }
    ]
  }
}

// Private DNS Zone for Container App Environment
resource privateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.azurewebsites.net'
  location: 'global'
}

// Private DNS Zone Group
resource privateDnsZoneGroup 'Microsoft.Network/privateDnsZoneGroups@2021-05-01' = {
  name: '${privateEndpoint.name}-pdzg'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'default'
        properties: {
          privateDnsZoneId: privateDnsZone.id
        }
      }
    ]
  }
  dependsOn: [
    privateEndpoint
    privateDnsZone
  ]
}


### Key Points:
1. **Parameters**: Only essential parameters are included to avoid over-parameterization.
2. **Resources**: The template includes resources for a Container App, its environment, a private endpoint, and a private DNS zone.
3. **Network Security**: The Container App is integrated with a virtual network via a private endpoint.
4. **Logging**: Log Analytics is configured for monitoring.
5. **Comments**: Comments are added for clarity.
6. **Best Practices**: Follows Azure Well-Architected Framework and Bicep best practices.

Feel free to adjust the parameters and resource configurations as per your specific requirements.
