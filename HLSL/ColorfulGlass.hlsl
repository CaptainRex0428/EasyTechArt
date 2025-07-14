// float3 Position
// float3 ViewDirection
// float3 NormalVector
// float3 ObjectPosition

// float Refraction

// float3 SurfaceColor
// float3 CenterColor
// float 

// float StepLength
// int StepCount


float StepUnit = StepLength / StepCount;
float StepDistance = .0f;

float RefractionVector = refract(ViewDirection,NormalVector,saturate(1-Refraction));

float3 SampledColor = 0.0f;

float3 SampledPosition;

for(int MarchingIdx = 0; MarchingIdx < StepCount; ++ MarchingIdx)
{
    SampledPosition = Position + StepDistance * RefractionVector;

    float SampleWeight = (1-(StepDistance / StepLength));

    SampledColor += Lerp(CenterColor,SurfaceColor,distance(SampledPosition,ObjectPosition)) * SampleWeight;

    StepDistance += StepUnit;
}

return SampledColor;