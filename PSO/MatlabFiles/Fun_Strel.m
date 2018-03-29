function [se] = Fun_Strel(type, dim, R, XYZ)


% Pawe³ Badura 2010
% Generacja elementu strukturalnego
% type - typ strel
% dim - wymiar strel
% R - promieñ strel
% XYZ - wymiary woksela (tam gdzie potrzebne)
% se - strel

switch (dim)
    case 2
        switch type
            case 'ellipsoid'
                Rvox = round([R R] * prod(XYZ));
                D = 2*Rvox + 1;
                S = Rvox + 1;
                se = zeros(D(1), D(2));
                for i = 1:S(1)
                    for j = 1:S(2)
                        se(i,j) = sqrt((XYZ(1)*(i-S(1)))^2 + (XYZ(2)*(j-S(2)))^2);
                    end
                end
                se(:,S(2):D(2)) = flipdim(se(:,1:S(2)), 2);
                se(S(1):D(1),:) = flipdim(se(1:S(1),:), 1);
                se = (se<=R);
                for i = D(2):-1:1
                    if (~nnz(se(:,i)))    se(:,i) = [];     end
                end                
                for i = D(1):-1:1
                    if (~nnz(se(i,:)))    se(i,:) = [];     end
                end                
                
            otherwise
                se = strel(type, R, 0);
                se = se.Neighborhood;
                return;
        end
    case 3
        switch type
            case 'ball'
                D = 2*R+1;
                se = zeros(D,D,D);
                se(R+1,R+1,R+1) = 1;
                se = bwdist(se);
                se = (se<=R);
            case 'linever'
                se = ones(2*R+1,1,1);
            case 'linehor'
                se = ones(1,2*R+1,1);
            case 'lineins'
                se = ones(1,1,2*R+1);
            case 'ellipsoid'
                Rvox = Fun_mm2vox([R R R], XYZ);
                D = 2*Rvox + 1;
                S = Rvox + 1;
                se = zeros(D(1), D(2), D(3));
                for i = 1:S(1)
                    for j = 1:S(2)
                        for k = 1:S(3)
                            se(i,j,k) = sqrt((XYZ(1)*(i-S(1)))^2 + (XYZ(2)*(j-S(2)))^2 + (XYZ(3)*(k-S(3)))^2);
                        end
                    end
                end
                se(:,:,S(3):D(3)) = flipdim(se(:,:,1:S(3)), 3);
                se(:,S(2):D(2),:) = flipdim(se(:,1:S(2),:), 2);
                se(S(1):D(1),:,:) = flipdim(se(1:S(1),:,:), 1);

                se = (se<=R);
                for i = D(3):-1:1
                    if (~nnz(se(:,:,i)))    se(:,:,i) = [];     end
                end                
                for i = D(2):-1:1
                    if (~nnz(se(:,i,:)))    se(:,i,:) = [];     end
                end                
                for i = D(1):-1:1
                    if (~nnz(se(i,:,:)))    se(i,:,:) = [];     end
                end                
        end
end
se = logical(se);