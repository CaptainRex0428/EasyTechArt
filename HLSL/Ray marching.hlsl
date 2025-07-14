// float3 InWorldPosition
// float3 InCameraPosition
// float3 InCameraVector
// float3 InObjectPosition

float3 RayOrigin = InWorldPosition;
float RayUnit = 5;
float3 RayStep = -InCameraVector * RayUnit;

for(int i = 0; i < 8; ++i)
{   
    RayOrigin += RayStep;
    float Dist = length(RayOrigin, InObjectPosition);
    if(Dist < 20)
    {
        return Dist/1000;
    }
}

return 0;
