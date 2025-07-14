//float2    UVs         (-1,1)
//float     EdgeLength  (0,1)

#define PI 3.1415926535

class MyCustomNode
{
    static float AntiAliasingStep(float3 Ramp, float3 Value)
    {
        float3 AAUnit = fwidth(Ramp);

        return smoothstep(Value-AAUnit*0.5,Value+AAUnit*0.5,Ramp);
    }
};


float angle30 = PI / 6;
float angle60 = PI / 3;

float k = sin(angle60) / sin(angle30);
float b1 = EdgeLength / (2 * cos(angle30));
float b2 = b1 * sin(angle30);

float RampLeft = UVs.y - (k * UVs.x - b1);
float RampRight = UVs.y - (-k * UVs.x - b1);
float RampBottom = UVs.y - b2;

return MyCustomNode::AntiAliasingStep(RampRight, 0) 
       * MyCustomNode::AntiAliasingStep(RampLeft, 0)
       * MyCustomNode::AntiAliasingStep(RampBottom, 0);

