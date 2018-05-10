function ref_img = python_load_ref_img( file_name )
addpath(genpath('MHA\mha'));
    MFileName = char(file_name);
%     try
        MInfo = mha_read_header(MFileName);
        MOrig = mha_read_volume(MInfo);
%     catch exc
%         disp('Nie ma obrysow dla tej serii!!');
%         return
%     end
    
    ref_img = double(MOrig);
end

