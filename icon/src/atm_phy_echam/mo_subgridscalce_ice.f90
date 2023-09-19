MODULE mo_subgridscale_ice

USE mo_kind,         ONLY : wp

IMPLICIT NONE
PRIVATE
PUBLIC :: subgridscale_ice


CONTAINS

SUBROUTINE subgridscale_ice (zxib ,zxlb, xisub)

!INTEGER, INTENT(IN)     :: jk, kproma, kbdim, klev
REAL(wp), INTENT(IN)    :: zxib
REAL(wp), INTENT(IN)    :: zxlb
REAL(wp), INTENT(INOUT) :: xisub     ! subgridscale ice
!REAL(wp), INTENT(INOUT) :: pxivar(kbdim,klev) ! cloud ice variance

!Local variables

REAL(wp) :: rand, icefrac, total,xisub2


! !cloud ice fraction

! total = zxib+zxlb

! if (total .gt. 0.0_wp) then
! icefrac = zxib/total
! else
! icefrac = 0.0_wp
! end if



CALL random_number(rand)

!write(*,*) rand

IF (zxib .GT. 1e-20_wp) THEN
      xisub = zxib+(zxib*((2._wp*rand)-1._wp)) 
      
ELSE
   xisub = 1e-20_wp
END IF


      xisub = MAX(MIN(xisub,2*zxib),1e-20_wp)



END SUBROUTINE subgridscale_ice

END MODULE mo_subgridscale_ice
